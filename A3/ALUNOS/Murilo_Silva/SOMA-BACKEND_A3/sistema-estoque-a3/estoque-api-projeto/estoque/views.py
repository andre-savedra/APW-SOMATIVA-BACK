from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Categoria, Marca, Setor, Produto, Escaninho
from .serializers import (
    CategoriaSerializer, MarcaSerializer, SetorSerializer,
    ProdutoSerializer, EscaninhoSerializer, UserSerializer
)
from .filters import ProdutoFilter
from .permissions import IsAdminOrReadOnly

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
    search_fields = ['letra', 'descricao']
    ordering_fields = ['letra', 'data_criacao']
    ordering = ['letra']

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.select_related('categoria', 'marca').prefetch_related('escaninhos__setor')
    serializer_class = ProdutoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProdutoFilter
    search_fields = ['nome', 'codigo_registro', 'codigo_barras']
    ordering_fields = ['nome', 'data_cadastro', 'valor_venda', 'custo']
    ordering = ['-data_cadastro']

    def update(self, request, *args, **kwargs):
        # Verificar se está tentando alterar o campo em_promocao
        if 'em_promocao' in request.data:
            if not request.user.is_staff:
                return Response(
                    {'detail': 'Apenas administradores podem alterar o status de promoção.'},
                    status=status.HTTP_403_FORBIDDEN
                )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        # Verificar se está tentando alterar o campo em_promocao
        if 'em_promocao' in request.data:
            if not request.user.is_staff:
                return Response(
                    {'detail': 'Apenas administradores podem alterar o status de promoção.'},
                    status=status.HTTP_403_FORBIDDEN
                )
        return super().partial_update(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def mais_antigos(self, request):
        """Endpoint para buscar os 10 produtos mais antigos no estoque"""
        produtos_antigos = self.get_queryset().order_by('data_cadastro')[:10]
        serializer = self.get_serializer(produtos_antigos, many=True)
        return Response({
            'count': len(produtos_antigos),
            'results': serializer.data
        })

    @action(detail=False, methods=['get'])
    def promocoes(self, request):
        """Endpoint para listar apenas produtos em promoção"""
        produtos_promocao = self.get_queryset().filter(em_promocao=True)
        page = self.paginate_queryset(produtos_promocao)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(produtos_promocao, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], permission_classes=[IsAdminOrReadOnly])
    def toggle_promocao(self, request, pk=None):
        """Endpoint específico para alterar status de promoção (apenas admin)"""
        produto = self.get_object()
        produto.em_promocao = not produto.em_promocao
        produto.save()
        
        serializer = self.get_serializer(produto)
        return Response({
            'message': f'Produto {"adicionado à" if produto.em_promocao else "removido da"} promoção.',
            'produto': serializer.data
        })

class EscaninhoViewSet(viewsets.ModelViewSet):
    queryset = Escaninho.objects.select_related('setor', 'produto__categoria', 'produto__marca')
    serializer_class = EscaninhoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['setor', 'produto', 'setor__letra']
    search_fields = ['codigo', 'setor__letra', 'produto__nome']
    ordering_fields = ['codigo', 'setor__letra', 'quantidade', 'data_criacao']
    ordering = ['setor__letra', 'codigo']

    @action(detail=False, methods=['get'])
    def vazios(self, request):
        """Listar escaninhos vazios"""
        escaninhos_vazios = self.get_queryset().filter(produto__isnull=True)
        page = self.paginate_queryset(escaninhos_vazios)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(escaninhos_vazios, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def ocupados(self, request):
        """Listar escaninhos ocupados"""
        escaninhos_ocupados = self.get_queryset().filter(produto__isnull=False, quantidade__gt=0)
        page = self.paginate_queryset(escaninhos_ocupados)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(escaninhos_ocupados, many=True)
        return Response(serializer.data)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'email', 'date_joined']
    ordering = ['username']