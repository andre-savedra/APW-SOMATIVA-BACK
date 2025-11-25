from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from .models import *
from .serializers import *
from .permissions import *

# ==================== FUNCIONÁRIOS ====================
class FuncionarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Funcionários
    Apenas ADMIN pode acessar (Requisito 11)
    """
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
    permission_classes = [IsAdmin]

# ==================== PRODUTOS ====================
class ProdutoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Produtos
    Admin pode criar/editar, outros apenas visualizar
    """
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['categoria']
    search_fields = ['nome', 'codigo']

# ==================== MÁQUINAS ====================
class MaquinaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Máquinas
    Apenas MANUTENÇÃO pode criar/editar (Requisito 8)
    Retorna dados com todas as manutenções (Requisito 4)
    """
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['nome', 'codigo']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsManutencao()]
        return [permissions.IsAuthenticated()]

# ==================== MANUTENÇÕES ====================
class ManutencaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Manutenções
    Apenas MANUTENÇÃO pode acessar (Requisito 8)
    """
    queryset = Manutencao.objects.select_related('maquina', 'funcionario').all()
    serializer_class = ManutencaoSerializer
    permission_classes = [IsManutencao]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['maquina']

# ==================== LOTES ====================
class LoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Lotes
    PRODUÇÃO pode fazer CRUD (Requisito 7)
    INSPEÇÃO vê apenas não inspecionados ou inspecionados por ele (Requisito 6)
    Suporta filtros de data, máquina e categoria (Requisito 5)
    Retorna dados detalhados com nome do inspetor (Requisito 3)
    """
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status_inspecao']
    
    def get_permissions(self):
        return True
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsProducao()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        queryset = Lote.objects.select_related('responsavel_inspecao').prefetch_related('itens').all()
        user = self.request.user
        
        # Requisito 6: Inspetores veem apenas lotes não inspecionados ou inspecionados por eles
        if user.is_authenticated and getattr(user, 'cargo', None) == 'INSPECAO':
            queryset = queryset.filter(
                Q(status_inspecao__isnull=True) | Q(responsavel_inspecao=user)
            )
        
        # Requisito 5: Filtro de produção reprovada por data, máquina e categoria
        data_inicio = self.request.query_params.get('data_inicio')
        data_fim = self.request.query_params.get('data_fim')
        maquina_id = self.request.query_params.get('maquina')
        categoria = self.request.query_params.get('categoria')
        
        if data_inicio and data_fim:
            queryset = queryset.filter(data_inicio__range=[data_inicio, data_fim])
        
        if maquina_id:
            queryset = queryset.filter(itens__maquina_id=maquina_id).distinct()
        
        if categoria:
            queryset = queryset.filter(itens__produto__categoria=categoria).distinct()
        
        return queryset

# ==================== ITENS DE PRODUÇÃO ====================
class ItemProducaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Itens de Produção
    PRODUÇÃO pode fazer CRUD (Requisito 7)
    """
    queryset = ItemProducao.objects.select_related('lote', 'produto', 'maquina').all()
    serializer_class = ItemProducaoSerializer
    permission_classes = [IsProducao]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['lote', 'produto', 'maquina']

# ==================== ENDPOINT PERSONALIZADO: MÁQUINAS COM MANUTENÇÃO PENDENTE ====================
class MaquinaManutencaoViewSet(viewsets.ViewSet):
    """
    ViewSet para identificar máquinas que precisam manutenção
    Apenas MANUTENÇÃO pode acessar (Requisito 9)
    Retorna máquinas com última manutenção há mais de 90 dias (3 meses)
    """
    permission_classes = [IsManutencao]
    
    @action(detail=False, methods=['get'], url_path='precisam-manutencao')
    def precisam_manutencao(self, request):
        """
        GET /api/maquinas-manutencao/precisam-manutencao/
        
        Retorna as máquinas que estão há mais de 90 dias sem manutenção.
        """
        tres_meses_atras = timezone.now() - timedelta(days=90)
        maquinas = Maquina.objects.prefetch_related('manutencoes').all()
        
        maquinas_precisam = []
        
        for maquina in maquinas:
            ultima_manutencao = maquina.manutencoes.order_by('-data_hora').first()
            
            if not ultima_manutencao or ultima_manutencao.data_hora < tres_meses_atras:
                dias_sem_manutencao = (
                    (timezone.now() - ultima_manutencao.data_hora).days 
                    if ultima_manutencao 
                    else None
                )
                
                maquinas_precisam.append({
                    'id': maquina.id,
                    'nome': maquina.nome,
                    'codigo': maquina.codigo,
                    'descricao': maquina.descricao,
                    'ultima_manutencao': ultima_manutencao.data_hora if ultima_manutencao else None,
                    'dias_sem_manutencao': dias_sem_manutencao if dias_sem_manutencao else 'Nunca foi feita',
                    'necessita_manutencao': True
                })
        
        return Response({
            'total': len(maquinas_precisam),
            'maquinas': maquinas_precisam
        }, status=status.HTTP_200_OK)

# ==================== ENDPOINT PERSONALIZADO: DASHBOARD DO LÍDER DE PRODUÇÃO ====================
class DashboardViewSet(viewsets.ViewSet):
    """
    ViewSet para Dashboard
    Apenas LÍDER DE PRODUÇÃO pode acessar (Requisito 10)
    Retorna estatísticas de peças aprovadas/reprovadas com filtros
    """
    permission_classes = [IsLiderProducao]
    
    @action(detail=False, methods=['get'], url_path='producao')
    def producao(self, request):
        """
        GET /api/dashboard/producao/
        
        Retorna estatísticas gerais da produção:
        - Total de peças aprovadas
        - Total de peças reprovadas
        - Filtros: data_inicio, data_fim, funcionario
        """
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        funcionario_id = request.query_params.get('funcionario')
        
        lotes = Lote.objects.all()
        
        if data_inicio and data_fim:
            lotes = lotes.filter(data_inicio__range=[data_inicio, data_fim])
        
        if funcionario_id:
            lotes = lotes.filter(responsavel_inspecao_id=funcionario_id)
        
        total_aprovados = ItemProducao.objects.filter(
            lote__in=lotes.filter(status_inspecao='Aprovado')
        ).count()
        
        total_reprovados = ItemProducao.objects.filter(
            lote__in=lotes.filter(status_inspecao='Reprovado')
        ).count()
        
        return Response({
            'total_pecas_aprovadas': total_aprovados,
            'total_pecas_reprovadas': total_reprovados,
            'total_lotes': lotes.count(),
            'filtros_aplicados': {
                'data_inicio': data_inicio,
                'data_fim': data_fim,
                'funcionario_id': funcionario_id
            }
        }, status=status.HTTP_200_OK)