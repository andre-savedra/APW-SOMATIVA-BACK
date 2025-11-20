
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import User, Produto, Lote, Maquina, Manutencao, ItemProduzido
from .serializers import *
from .filters import *

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['ADMIN', 'CHEFE_PRODUCAO']:
            return User.objects.all()
        return User.objects.filter(id=user.id)

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    # permission_classes = [permissions.IsAuthenticated]

class LoteViewSet(viewsets.ModelViewSet):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LoteFilter
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Lote.objects.all().select_related('produto', 'responsavel_inspecao').prefetch_related('itens')
        
        # Funcionários de inspeção veem apenas não inspecionados ou inspecionados por eles
        if user.role == 'INSPECAO':
            return queryset.filter(
                Q(status_inspecao='') | Q(responsavel_inspecao=user) | Q(responsavel_inspecao__isnull=True)
            )
        return queryset

    @action(detail=False, methods=['get'])
    def producao_reprovada(self, request):
        """Endpoint para produção reprovada com filtros"""
        user = self.request.user
        if user.role not in ['ADMIN', 'CHEFE_PRODUCAO', 'INSPECAO']:
            return Response({"error": "Permissão negada"}, status=status.HTTP_403_FORBIDDEN)
        
        filtered_qs = ProducaoReprovadaFilter(request.GET, queryset=self.get_queryset()).qs
        serializer = self.get_serializer(filtered_qs, many=True)
        return Response(serializer.data)

class MaquinaViewSet(viewsets.ModelViewSet):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MaquinaFilter
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Maquina.objects.all().prefetch_related('manutencoes__funcionario')

    def perform_create(self, serializer):
        user = self.request.user
        if user.role not in ['ADMIN', 'MANUTENCAO']:
            raise permissions.PermissionDenied("Apenas funcionários de manutenção podem criar máquinas")
        serializer.save()

    def perform_update(self, serializer):
        user = self.request.user
        if user.role not in ['ADMIN', 'MANUTENCAO']:
            raise permissions.PermissionDenied("Apenas funcionários de manutenção podem editar máquinas")
        serializer.save()

    @action(detail=False, methods=['get'])
    def precisa_manutencao(self, request):
        """Endpoint para máquinas que precisam de manutenção"""
        user = self.request.user
        if user.role not in ['ADMIN', 'MANUTENCAO']:
            return Response({"error": "Permissão negada"}, status=status.HTTP_403_FORBIDDEN)
        
        dois_meses_atras = timezone.now() - timedelta(days=60)
        maquinas = Maquina.objects.filter(
            Q(manutencoes__isnull=True) | 
            Q(manutencoes__data_hora__lt=dois_meses_atras)
        ).distinct()
        
        serializer = self.get_serializer(maquinas, many=True)
        return Response(serializer.data)

class ManutencaoViewSet(viewsets.ModelViewSet):
    queryset = Manutencao.objects.all()
    serializer_class = ManutencaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role not in ['ADMIN', 'MANUTENCAO']:
            raise permissions.PermissionDenied("Apenas funcionários de manutenção podem criar manutenções")
        serializer.save(funcionario=user)

    def perform_update(self, serializer):
        user = self.request.user
        if user.role not in ['ADMIN', 'MANUTENCAO']:
            raise permissions.PermissionDenied("Apenas funcionários de manutenção podem editar manutenções")
        serializer.save()

class ItemProduzidoViewSet(viewsets.ModelViewSet):
    queryset = ItemProduzido.objects.all()
    serializer_class = ItemProduzidoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role not in ['ADMIN', 'PRODUCAO']:
            raise permissions.PermissionDenied("Apenas funcionários de produção podem criar itens produzidos")
        serializer.save()

    def perform_update(self, serializer):
        user = self.request.user
        if user.role not in ['ADMIN', 'PRODUCAO']:
            raise permissions.PermissionDenied("Apenas funcionários de produção podem editar itens produzidos")
        serializer.save()

class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def producao(self, request):
        """Endpoint de dashboard para chefes de produção"""
        user = self.request.user
        if user.role not in ['ADMIN', 'CHEFE_PRODUCAO']:
            return Response({"error": "Permissão negada"}, status=status.HTTP_403_FORBIDDEN)
        
        # Filtros
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')
        funcionario_id = request.GET.get('funcionario')
        
        queryset = Lote.objects.all()
        
        if data_inicio and data_fim:
            queryset = queryset.filter(data_inicio__date__range=[data_inicio, data_fim])
        
        if funcionario_id:
            queryset = queryset.filter(responsavel_inspecao_id=funcionario_id)
        
        total_aprovadas = queryset.filter(status_inspecao='Aprovado').count()
        total_reprovadas = queryset.filter(status_inspecao='Reprovado').count()
        total_geral = total_aprovadas + total_reprovadas
        taxa_aprovacao = (total_aprovadas / total_geral * 100) if total_geral > 0 else 0
        
        data = {
            'total_aprovadas': total_aprovadas,
            'total_reprovadas': total_reprovadas,
            'taxa_aprovacao': round(taxa_aprovacao, 2),
            'periodo_inicio': data_inicio,
            'periodo_fim': data_fim
        }
        
        serializer = DashboardSerializer(data)
        return Response(serializer.data)