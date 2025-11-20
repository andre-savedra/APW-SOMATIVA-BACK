from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Producao
from ..serializers import ProducaoSerializer
from ..filters import ProducaoFilter
from ..utils import is_Producao, is_Admin, is_Inspecao, is_LiderProducao
from rest_framework.decorators import action 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ProducaoView(ModelViewSet):
    queryset = Producao.objects.all()
    serializer_class = ProducaoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProducaoFilter
    permission_classes = [IsAuthenticated] 

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def dashboard(self, request):
        user = request.user
        if not is_LiderProducao(user):
            return Response({"detail": "Apenas líderes de produção podem acessar o dashboard."}, status=403)
        queryset = Producao.objects.all() 
        data_inicio = request.query_params.get("data_inicio")
        data_fim = request.query_params.get("data_fim")
        funcionario_id = request.query_params.get("funcionario_id")
        if data_inicio:
            queryset = queryset.filter(data_inspecao__gte=data_inicio) 
        if data_fim:
            queryset = queryset.filter(data_inspecao__lte=data_fim)  
        if funcionario_id:
            queryset = queryset.filter(responsavel_producao_id=funcionario_id)
        aprovadas = queryset.filter(status="Aprovado").count() 
        reprovadas = queryset.filter(status="Reprovado").count()
        return Response({
            "aprovadas": aprovadas,
            "reprovadas": reprovadas
        })