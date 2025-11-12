from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import *
from .serializers import *


# 2 = CRUDS PRINCIPAIS#

class CargoView(ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer


class FuncionarioView(ModelViewSet):
    queryset = Funcionario.objects.select_related('cargo').all()
    serializer_class = FuncionarioSerializer


class MaquinaView(ModelViewSet):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer


class ManutencaoView(ModelViewSet):
    queryset = Manutencao.objects.select_related('maquina', 'funcionario').all()
    serializer_class = ManutencaoSerializer


class ProdutoView(ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer


class LoteView(ModelViewSet):
    queryset = Lote.objects.select_related('produto', 'responsavel_inspecao').prefetch_related('itens').all()
    serializer_class = LoteSerializer


class ItemLoteView(ModelViewSet):
    queryset = ItemLote.objects.select_related('lote', 'maquina').all()
    serializer_class = ItemLoteSerializer


#5 - ENDPOINT PERSONALIZADO #


@api_view(['GET'])
def lotes_reprovados(request):
    """
    Retorna só lotes reprovados, com filtros opcionais:
    - data_inicio e data_fim (intervalo de datas)
    - maquina (ID)
    - categoria (nome da categoria do produto)
    """
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
