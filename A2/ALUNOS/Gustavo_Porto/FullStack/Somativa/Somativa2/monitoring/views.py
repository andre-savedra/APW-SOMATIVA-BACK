from datetime import datetime, timedelta
from django.db.models import Max, Q
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Categoria,
    Produto,
    Funcionario,
    Maquina,
    Manutencao,
    Lote,
    ItemProducao,
    InspecaoStatus,
)
from .serializers import (
    CategoriaSerializer,
    ProdutoSerializer,
    FuncionarioSerializer,
    MaquinaSerializer,
    ManutencaoSerializer,
    LoteSerializer,
    ItemProducaoSerializer,
)
from .permissions import (
    IsMaintenanceOrReadOnly,
    IsProductionOrReadOnly,
    IsAdminOnly,
    IsLeaderOnly,
    get_user_role,
)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer


class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.select_related('user').all()
    serializer_class = FuncionarioSerializer
    permission_classes = [IsAdminOnly]


class MaquinaDetailSerializer(MaquinaSerializer):
    manutencoes = ManutencaoSerializer(many=True, read_only=True)

    class Meta(MaquinaSerializer.Meta):
        fields = MaquinaSerializer.Meta.fields + ['manutencoes']


class MaquinaViewSet(viewsets.ModelViewSet):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer
    permission_classes = [IsMaintenanceOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return MaquinaDetailSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['get'], url_path='precisam-manutencao', permission_classes=[IsMaintenanceOrReadOnly])
    def precisam_manutencao(self, request):
        limite = timezone.now() - timedelta(days=90)
        maquinas = (
            Maquina.objects.annotate(ultima=Max('manutencoes__data_hora'))
            .filter(Q(ultima__lt=limite) | Q(ultima__isnull=True))
        )
        serializer = self.get_serializer(maquinas, many=True)
        return Response(serializer.data)


class ManutencaoViewSet(viewsets.ModelViewSet):
    queryset = Manutencao.objects.select_related('maquina', 'funcionario').all()
    serializer_class = ManutencaoSerializer
    permission_classes = [IsMaintenanceOrReadOnly]


class LoteViewSet(viewsets.ModelViewSet):
    queryset = Lote.objects.select_related('produto', 'inspetor', 'produto__categoria').prefetch_related('itens')
    serializer_class = LoteSerializer
    permission_classes = [IsProductionOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        role = get_user_role(self.request.user)
        if role == 'INSPECAO':
            qs = qs.filter(Q(status_inspecao__isnull=True) | Q(inspetor__user=self.request.user))
        return qs

    @action(detail=False, methods=['get'], url_path='reprovados')
    def reprovados(self, request):
        qs = self.get_queryset().filter(status_inspecao=InspecaoStatus.REPROVADO)

        inicio = request.query_params.get('inicio')
        fim = request.query_params.get('fim')
        maquina_id = request.query_params.get('maquina')
        categoria_id = request.query_params.get('categoria')

        def parse_dt(val):
            if not val:
                return None
            try:
                
                return datetime.fromisoformat(val)
            except Exception:
                try:
                    
                    return datetime.fromisoformat(val + 'T00:00:00')
                except Exception:
                    return None

        if inicio:
            dt_inicio = parse_dt(inicio)
            if dt_inicio:
                qs = qs.filter(data_inspecao__gte=dt_inicio)
        if fim:
            dt_fim = parse_dt(fim)
            if dt_fim:
                qs = qs.filter(data_inspecao__lte=dt_fim)

        if maquina_id:
            qs = qs.filter(itens__maquina_id=maquina_id)
        if categoria_id:
            qs = qs.filter(produto__categoria_id=categoria_id)

        qs = qs.distinct()
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class ItemProducaoViewSet(viewsets.ModelViewSet):
    queryset = ItemProducao.objects.select_related('lote', 'maquina').all()
    serializer_class = ItemProducaoSerializer
    permission_classes = [IsProductionOrReadOnly]


class DashboardView(APIView):
    permission_classes = [IsLeaderOnly]

    def get(self, request):
        inicio = request.query_params.get('inicio')
        fim = request.query_params.get('fim')
        funcionario_id = request.query_params.get('funcionario')

        qs_lotes = Lote.objects.filter(status_inspecao__in=[InspecaoStatus.APROVADO, InspecaoStatus.REPROVADO])

        def parse_dt(val):
            if not val:
                return None
            try:
                return datetime.fromisoformat(val)
            except Exception:
                try:
                    return datetime.fromisoformat(val + 'T00:00:00')
                except Exception:
                    return None

        if inicio:
            dt_inicio = parse_dt(inicio)
            if dt_inicio:
                qs_lotes = qs_lotes.filter(data_inspecao__gte=dt_inicio)
        if fim:
            dt_fim = parse_dt(fim)
            if dt_fim:
                qs_lotes = qs_lotes.filter(data_inspecao__lte=dt_fim)

        if funcionario_id:
            qs_lotes = qs_lotes.filter(inspetor_id=funcionario_id)

       
        itens = ItemProducao.objects.filter(lote__in=qs_lotes)
        aprovadas = itens.filter(lote__status_inspecao=InspecaoStatus.APROVADO).count()
        reprovadas = itens.filter(lote__status_inspecao=InspecaoStatus.REPROVADO).count()

        return Response({'aprovadas': aprovadas, 'reprovadas': reprovadas})
