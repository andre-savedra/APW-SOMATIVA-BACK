from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Categoria, Marca, Setor, Produto, Escaninho
from .serializers import (
    CategoriaSerializer, MarcaSerializer, SetorSerializer, 
    ProdutoSerializer, EscaninhoSerializer
)
from .filters import ProdutoFilter 

# crud categoria:
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


    @action(detail=True, methods=['get'])
    def produtos(self, request, pk=None):
        categoria = self.get_object()
        produtos = Produto.objects.filter(categoria=categoria)
        serializer = ProdutoSerializer(produtos, many=True)
        return Response(serializer.data)

# crud marca:
class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer

# crud setor:
class SetorViewSet(viewsets.ModelViewSet):
    queryset = Setor.objects.all()
    serializer_class = SetorSerializer


    @action(detail=True, methods=['get'])
    def escaninhos(self, request, pk=None):
        setor = self.get_object()
        escaninhos = Escaninho.objects.filter(setor=setor)
        serializer = EscaninhoSerializer(escaninhos, many=True)
        return Response(serializer.data)

# crud escaninho:
class EscaninhoViewSet(viewsets.ModelViewSet):
    queryset = Escaninho.objects.all()
    serializer_class = EscaninhoSerializer

# crud produto:
class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    
    # fitros:
    filterset_class = ProdutoFilter
    
    # busca pelo codigo de barras:
    search_fields = ['codigo_barras_numerico', 'nome']
    
    # ordenação:
    ordering_fields = ['data_cadastro', 'valor_venda']

    @action(detail=False, methods=['get'])
    def mais_antigos(self, request):
        produtos_antigos = Produto.objects.order_by('data_cadastro')[:10]
        serializer = self.get_serializer(produtos_antigos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def definir_promocao(self, request, pk=None):
        produto = self.get_object()
        novo_estado = request.data.get('em_promocao')

        if novo_estado is None or not isinstance(novo_estado, bool):
            return Response(
                {"erro": "Forneça 'em_promocao' (true/false) no corpo."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        produto.em_promocao = novo_estado
        produto.save()
        serializer = self.get_serializer(produto)
        return Response(serializer.data)