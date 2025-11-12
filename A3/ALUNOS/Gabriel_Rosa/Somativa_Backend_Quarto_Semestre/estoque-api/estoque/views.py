from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

from .models import Categoria, Marca, Setor, Produto, Escaninho
from .serializers import (
    CategoriaSerializer, MarcaSerializer, SetorSerializer, 
    ProdutoListSerializer, ProdutoCreateUpdateSerializer, ProdutoPromocaoSerializer,
    EscaninhoDetailSerializer, EscaninhoCreateUpdateSerializer
)
from .filters import ProdutoFilter, EscaninhoFilter
from .permissions import IsAdminOrReadOnly, IsAdminForPromotion

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome']
    ordering_fields = ['nome', 'data_registro']
    ordering = ['nome']

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'cnpj']
    ordering_fields = ['nome', 'data_inclusao']
    ordering = ['nome']

class SetorViewSet(viewsets.ModelViewSet):
    queryset = Setor.objects.all()
    serializer_class = SetorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'data_criacao']
    ordering = ['nome']

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.select_related('categoria', 'marca').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProdutoFilter
    search_fields = ['nome', 'codigo_registro', 'codigo_barras']
    ordering_fields = ['data_cadastro', 'valor_venda', 'nome']
    ordering = ['-data_cadastro']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProdutoCreateUpdateSerializer
        elif self.action == 'promocao':
            return ProdutoPromocaoSerializer
        return ProdutoListSerializer
    
    def get_permissions(self):
        if self.action == 'promocao':
            self.permission_classes = [IsAdminForPromotion]
        return [permission() for permission in self.permission_classes]
    
    @action(detail=True, methods=['patch'], url_path='promocao')
    def promocao(self, request, pk=None):
        """Endpoint específico para alterar status de promoção (apenas admins)"""
        try:
            produto = self.get_object()
            serializer = self.get_serializer(produto, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        
            # Retorna produto completo após atualização
            response_serializer = ProdutoListSerializer(produto)
            return Response(response_serializer.data)
        except Exception as e:
            return Response(
                {"error": "Erro ao processar promoção", "detail": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    @action(detail=False, methods=['get'], url_path='mais-antigos')
    def mais_antigos(self, request):
        """Endpoint para retornar os 10 produtos mais antigos"""
        produtos = self.queryset.order_by('data_cadastro')[:10]
        serializer = self.get_serializer(produtos, many=True)
        return Response({
            'count': len(produtos),
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'], url_path='em-promocao')
    def em_promocao(self, request):
        """Endpoint para retornar apenas produtos em promoção"""
        produtos = self.queryset.filter(em_promocao=True)
        page = self.paginate_queryset(produtos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(produtos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='buscar-codigo-barras')
    def buscar_codigo_barras(self, request):
        """Busca produtos por código de barras (busca parcial)"""
        codigo = request.query_params.get('codigo', '')
        if not codigo:
            return Response(
                {'error': 'Parâmetro "codigo" é obrigatório'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Busca parcial no código de barras
        produtos = self.queryset.filter(codigo_barras__icontains=codigo)
        page = self.paginate_queryset(produtos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(produtos, many=True)
        return Response(serializer.data)

class EscaninhoViewSet(viewsets.ModelViewSet):
    queryset = Escaninho.objects.select_related('setor', 'produto__categoria', 'produto__marca').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EscaninhoFilter
    search_fields = ['codigo', 'setor__nome', 'produto__nome']
    ordering_fields = ['codigo', 'setor__nome', 'data_criacao', 'quantidade']
    ordering = ['setor__nome', 'codigo']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EscaninhoCreateUpdateSerializer
        return EscaninhoDetailSerializer
    
    @action(detail=False, methods=['get'], url_path='com-produtos')
    def com_produtos(self, request):
        """Retorna apenas escaninhos que têm produtos"""
        escaninhos = self.queryset.filter(produto__isnull=False, quantidade__gt=0)
        page = self.paginate_queryset(escaninhos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(escaninhos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='vazios')
    def vazios(self, request):
        """Retorna apenas escaninhos vazios"""
        escaninhos = self.queryset.filter(Q(produto__isnull=True) | Q(quantidade=0))
        page = self.paginate_queryset(escaninhos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(escaninhos, many=True)
        return Response(serializer.data)