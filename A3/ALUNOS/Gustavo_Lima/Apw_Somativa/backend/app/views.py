from django.shortcuts import render


from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Categoria, Marca, Produto, Setor, Escaninho
from .serializers import (
    CategoriaSerializer, MarcaSerializer, ProdutoSerializer,
    ProdutoListSerializer, SetorSerializer, SetorListSerializer,
    EscaninhoSerializer, EscaninhoListSerializer
)
from .permissons import IsAdminOrReadOnly


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]


class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [IsAuthenticated]


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.select_related('categoria', 'marca').all()
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['data_cadastro', 'valor_venda']
    ordering = ['-data_cadastro']
    
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ProdutoListSerializer
        return ProdutoSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por setor
        setor = self.request.query_params.get('setor', None)
        if setor:
            queryset = queryset.filter(escaninhos__setor__letra=setor).distinct()
        
        # Filtro por escaninho
        escaninho = self.request.query_params.get('escaninho', None)
        if escaninho:
            queryset = queryset.filter(escaninhos__codigo=escaninho).distinct()
        
        # Filtro por marca
        marca = self.request.query_params.get('marca', None)
        if marca:
            queryset = queryset.filter(marca__id=marca)
        
        # Filtro por código de produto
        codigo = self.request.query_params.get('codigo', None)
        if codigo:
            queryset = queryset.filter(codigo_registro=codigo)
        
        # Filtro por código de barras (busca parcial)
        codigo_barras = self.request.query_params.get('codigo_barras', None)
        if codigo_barras:
            queryset = queryset.filter(codigo_barras__icontains=codigo_barras)
        
        # Filtro por promoção
        em_promocao = self.request.query_params.get('em_promocao', None)
        if em_promocao is not None:
            if em_promocao.lower() in ['true', '1', 'sim']:
                queryset = queryset.filter(em_promocao=True)
            elif em_promocao.lower() in ['false', '0', 'nao', 'não']:
                queryset = queryset.filter(em_promocao=False)
        
        return queryset
    
    def update(self, request, *args, **kwargs):
        # Verifica se está tentando alterar em_promocao
        if 'em_promocao' in request.data:
            if not request.user.groups.filter(name='Admin').exists():
                return Response(
                    {'error': 'Apenas administradores podem colocar produtos em promoção'},
                    status=status.HTTP_403_FORBIDDEN
                )
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        # Verifica se está tentando alterar em_promocao
        if 'em_promocao' in request.data:
            if not request.user.groups.filter(name='Admin').exists():
                return Response(
                    {'error': 'Apenas administradores podem colocar produtos em promoção'},
                    status=status.HTTP_403_FORBIDDEN
                )
        return super().partial_update(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def mais_antigos(self, request):
        """Retorna os 10 produtos mais antigos no estoque"""
        produtos = self.get_queryset().order_by('data_cadastro')[:10]
        serializer = self.get_serializer(produtos, many=True)
        return Response(serializer.data)


class SetorViewSet(viewsets.ModelViewSet):
    queryset = Setor.objects.prefetch_related('escaninhos__produto__categoria', 'escaninhos__produto__marca').all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return SetorListSerializer
        return SetorSerializer


class EscaninhoViewSet(viewsets.ModelViewSet):
    queryset = Escaninho.objects.select_related('setor', 'produto__categoria', 'produto__marca').all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return EscaninhoListSerializer
        return EscaninhoSerializer

# Create your views here.
