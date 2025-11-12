from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models.equipment import Produto
from ..serializers.equipment import ProdutoSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['codigo_barras', 'codigo', 'marca__nome', 'escaninho__setor__nome']
    ordering_fields = ['data_cadastro', 'valor']

    def get_queryset(self):
        queryset = super().get_queryset()
        setor = self.request.query_params.get('setor')
        escaninho = self.request.query_params.get('escaninho')
        marca = self.request.query_params.get('marca')
        promocao = self.request.query_params.get('promocao')

        if setor:
            queryset = queryset.filter(escaninho__setor__id=setor)
        if escaninho:
            queryset = queryset.filter(escaninho_id=escaninho)
        if marca:
            queryset = queryset.filter(marca_id=marca)
        if promocao:
            queryset = queryset.filter(promocao=True)

        return queryset

    def perform_update(self, serializer):
        user = self.request.user
        if 'promocao' in self.request.data and not user.is_staff:
            raise PermissionError("Apenas administradores podem alterar promoção.")
        serializer.save()

    @action(detail=False, methods=['get'])
    def mais_antigos(self, request):
        antigos = Produto.objects.order_by('data_cadastro')[:10]
        serializer = self.get_serializer(antigos, many=True)
        return Response(serializer.data)