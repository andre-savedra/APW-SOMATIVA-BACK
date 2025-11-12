from rest_framework import viewsets, permissions, filters
from .permissions import IsChefeProducao, IsManutencao, IsInspecao, IsOwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Funcionario, Linha, OrdemProducao, Registro, Alerta, Manutencao
from .serializers import (
    FuncionarioSerializer, LinhaSerializer, OrdemProducaoSerializer,
    RegistroSerializer, AlertaSerializer, ManutencaoSerializer
)

from .models import Produto, Maquina, ManutencaoMaquina, Lote, ItemProducao
from .serializers import (
    ProdutoSerializer, MaquinaSerializer, ManutencaoMaquinaSerializer,
    LoteSerializer, ItemProducaoSerializer
)

class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'email', 'numero_registro', 'cpf']
    ordering_fields = ['nome', 'data_contratacao', 'cargo']

class LinhaViewSet(viewsets.ModelViewSet):
    queryset = Linha.objects.all()
    serializer_class = LinhaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['nome', 'descricao']
    filterset_fields = ['ativa']

class OrdemProducaoViewSet(viewsets.ModelViewSet):
    queryset = OrdemProducao.objects.all()
    serializer_class = OrdemProducaoSerializer
    permission_classes = [permissions.IsAuthenticated, IsChefeProducao]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['numero', 'produto']
    filterset_fields = ['status', 'linha', 'responsavel']
    ordering_fields = ['data_criacao', 'data_inicio', 'data_conclusao']

    @action(detail=True, methods=['post'])
    def iniciar_producao(self, request, pk=None):
        ordem = self.get_object()
        if ordem.status == OrdemProducao.Status.PENDENTE:
            ordem.status = OrdemProducao.Status.EM_PRODUCAO
            ordem.data_inicio = timezone.now()
            ordem.save()
            return Response({'status': 'Produção iniciada'})
        return Response({'error': 'Operação não permitida'}, status=400)

    @action(detail=True, methods=['post'])
    def concluir_producao(self, request, pk=None):
        ordem = self.get_object()
        if ordem.status == OrdemProducao.Status.EM_PRODUCAO:
            ordem.status = OrdemProducao.Status.CONCLUIDA
            ordem.data_conclusao = timezone.now()
            ordem.save()
            return Response({'status': 'Produção concluída'})
        return Response({'error': 'Operação não permitida'}, status=400)

class RegistroViewSet(viewsets.ModelViewSet):
    queryset = Registro.objects.all()
    serializer_class = RegistroSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['ordem_producao', 'funcionario', 'tipo']
    ordering_fields = ['data_hora']

    def perform_create(self, serializer):
        registro = serializer.save()
        if registro.tipo == Registro.TipoRegistro.PRODUCAO:
            ordem = registro.ordem_producao
            ordem.quantidade_produzida += registro.quantidade
            ordem.save()

class AlertaViewSet(viewsets.ModelViewSet):
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['titulo', 'descricao']
    filterset_fields = ['linha', 'prioridade', 'resolvido']
    ordering_fields = ['data_criacao', 'prioridade']

    @action(detail=True, methods=['post'])
    def resolver(self, request, pk=None):
        alerta = self.get_object()
        if not alerta.resolvido:
            alerta.resolvido = True
            alerta.data_resolucao = timezone.now()
            alerta.resolvido_por = request.user
            alerta.observacoes_resolucao = request.data.get('observacoes', '')
            alerta.save()
            return Response({'status': 'Alerta resolvido'})
        return Response({'error': 'Alerta já resolvido'}, status=400)

class ManutencaoViewSet(viewsets.ModelViewSet):
    queryset = Manutencao.objects.all()
    serializer_class = ManutencaoSerializer
    permission_classes = [permissions.IsAuthenticated, IsManutencao]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['linha', 'tipo', 'status', 'responsavel']
    ordering_fields = ['data_agendada', 'data_inicio', 'data_conclusao']

    @action(detail=True, methods=['post'])
    def iniciar(self, request, pk=None):
        manutencao = self.get_object()
        if manutencao.status == Manutencao.Status.AGENDADA:
            manutencao.status = Manutencao.Status.EM_ANDAMENTO
            manutencao.data_inicio = timezone.now()
            manutencao.save()
            return Response({'status': 'Manutenção iniciada'})
        return Response({'error': 'Operação não permitida'}, status=400)

    @action(detail=True, methods=['post'])
    def concluir(self, request, pk=None):
        manutencao = self.get_object()
        if manutencao.status == Manutencao.Status.EM_ANDAMENTO:
            manutencao.status = Manutencao.Status.CONCLUIDA
            manutencao.data_conclusao = timezone.now()
            manutencao.save()
            return Response({'status': 'Manutenção concluída'})
        return Response({'error': 'Operação não permitida'}, status=400)


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'codigo', 'categoria']
    ordering_fields = ['nome', 'codigo']


class MaquinaViewSet(viewsets.ModelViewSet):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'codigo']
    ordering_fields = ['nome', 'data_criacao']


class ManutencaoMaquinaViewSet(viewsets.ModelViewSet):
    queryset = ManutencaoMaquina.objects.all()
    serializer_class = ManutencaoMaquinaSerializer
    permission_classes = [permissions.IsAuthenticated, IsManutencao]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['maquina', 'responsavel']
    ordering_fields = ['data_hora']


class LoteViewSet(viewsets.ModelViewSet):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['codigo', 'produto__nome']
    filterset_fields = ['produto', 'status_inspecao']
    ordering_fields = ['data_hora_inicio', 'data_hora_final']

    @action(detail=False, methods=['get'], url_path='buscar-por-codigo')
    def buscar_por_codigo(self, request):
        codigo = request.query_params.get('codigo')
        if not codigo:
            return Response({'error': 'Parâmetro codigo é requerido'}, status=400)
        try:
            lote = Lote.objects.get(codigo=codigo)
        except Lote.DoesNotExist:
            return Response({'error': 'Lote não encontrado'}, status=404)
        serializer = self.get_serializer(lote)
        return Response(serializer.data)


class ItemProducaoViewSet(viewsets.ModelViewSet):
    queryset = ItemProducao.objects.all()
    serializer_class = ItemProducaoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['lote', 'produto', 'maquina']
    ordering_fields = ['data_hora']
