from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Produto, Categoria
from .serializers import ProdutoSerializer, CategoriaSerializer

# Listagem de categorias
class CategoriaListView(generics.ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

# Listagem de produtos
class ProdutoListView(generics.ListAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

# Detalhe de um produto
class ProdutoDetailView(generics.RetrieveAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
