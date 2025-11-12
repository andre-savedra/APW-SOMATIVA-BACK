from rest_framework import viewsets
from .models import Funcionario, Producao, Lote, Maquina, Produto
from .serializers import FuncionarioSerializer, ProducaoSerializer, LoteSerializer, MaquinaSerializer, ProdutoSerializer

# ViewSet para Funcionario
class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
    # Permissões podem ser ajustadas conforme necessário, exemplo:
    # permission_classes = [permissions.IsAuthenticated]

# ViewSet para Producao
class ProducaoViewSet(viewsets.ModelViewSet):
    queryset = Producao.objects.all()
    serializer_class = ProducaoSerializer

    # Exemplo de filtro para a produção
    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtros de data, máquina, categoria podem ser passados via query params
        data_inicio = self.request.query_params.get('data_inicio', None)
        data_fim = self.request.query_params.get('data_fim', None)
        maquina = self.request.query_params.get('maquina', None)
        categoria = self.request.query_params.get('categoria', None)

        if data_inicio and data_fim:
            queryset = queryset.filter(data_producao__range=[data_inicio, data_fim])
        
        if maquina:
            queryset = queryset.filter(maquina__id=maquina)
        
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        
        return queryset

# ViewSet para Lote
class LoteViewSet(viewsets.ModelViewSet):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer

# ViewSet para Maquina
class MaquinaViewSet(viewsets.ModelViewSet):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer

# ViewSet para Produto
class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
