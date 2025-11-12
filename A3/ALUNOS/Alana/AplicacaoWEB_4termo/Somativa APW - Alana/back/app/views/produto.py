from rest_framework.viewsets import ModelViewSet
from ..models import Produto
from ..serializers import ProdutoSerializer
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from ..filters.produto_filter import ProdutoFilter 


class ProdutoView(ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    filterset_class = ProdutoFilter 