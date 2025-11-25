from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from datetime import timedelta
from django.utils.timezone import now
from .models import *
from .serializers import *
from .permissions import IsLiderProducao, IsManutencaoOrReadOnly, IsProducaoOrReadOnly

# 2 - CRUDS PRINCIPAIS

class CargoView(ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer


class FuncionarioView(ModelViewSet):
    queryset = Funcionario.objects.select_related('cargo').all()
    serializer_class = FuncionarioSerializer


# --- (Regra 8) ---
class MaquinaView(ModelViewSet):
    permission_classes = [IsAuthenticated, IsManutencaoOrReadOnly]
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer


class ManutencaoView(ModelViewSet):
    permission_classes = [IsAuthenticated, IsManutencaoOrReadOnly]
    queryset = Manutencao.objects.select_related('maquina', 'funcionario').all()
    serializer_class = ManutencaoSerializer


class ProdutoView(ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer



# 6 E 7 - Lotes (inspeção + produção)

class LoteView(ModelViewSet):
    permission_classes = [IsAuthenticated, IsProducaoOrReadOnly]
    queryset = Lote.objects.select_related('produto', 'responsavel_inspecao').prefetch_related('itens').all()
    serializer_class = LoteSerializer

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()

        # --- Regra inspeção ---
        if not user.is_authenticated:
            return Lote.objects.none()

        if user.groups.filter(name__iexact='INSPECAO').exists():
            return qs.filter(
                Q(status_inspecao__isnull=True) | Q(status_inspecao='') |
                Q(responsavel_inspecao__user=user)
            ).distinct()

        return qs


class ItemLoteView(ModelViewSet):
    permission_classes = [IsAuthenticated, IsProducaoOrReadOnly]
    queryset = ItemLote.objects.select_related('lote', 'maquina').all()
    serializer_class = ItemLoteSerializer


# 5 - Lotes reprovados

@api_view(['GET'])
def lotes_reprovados(request):
    lotes = Lote.objects.filter(status_inspecao="Reprovado")

    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    maquina_id = request.GET.get('maquina')
    categoria = request.GET.get('categoria')

    if data_inicio and data_fim:
        lotes = lotes.filter(data_inicio__range=[data_inicio, data_fim])
    if categoria:
        lotes = lotes.filter(produto__categoria__icontains=categoria)
    if maquina_id:
        lotes = lotes.filter(itens__maquina__id=maquina_id).distinct()

    serializer = LoteSerializer(lotes, many=True)
    return Response(serializer.data)


# 9 - Maquinas para manutenção

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsManutencaoOrReadOnly])
def maquinas_precisam_manutencao(request):
    limite = now() - timedelta(days=90)
    maquinas = Maquina.objects.filter(
        manutencoes__data_hora__lt=limite
    ).distinct()
    serializer = MaquinaSerializer(maquinas, many=True)
    return Response(serializer.data)


# 10 - Lider Produção

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsLiderProducao])
def dashboard_producao(request):
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    funcionario_id = request.GET.get('funcionario')

    lotes = Lote.objects.all()
    if data_inicio and data_fim:
        lotes = lotes.filter(data_inicio__range=[data_inicio, data_fim])
    if funcionario_id:
        lotes = lotes.filter(responsavel_inspecao__id=funcionario_id)

    total_aprovados = lotes.filter(status_inspecao="Aprovado").count()
    total_reprovados = lotes.filter(status_inspecao="Reprovado").count()

    return Response({
        "total_aprovados": total_aprovados,
        "total_reprovados": total_reprovados
    })
