from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Lote, Item
from ..serializers import LoteSerializer
from ..permissions import Producao, Admin, LiderProducao, Authenticated
from app.filter import LoteFilter

class LoteView(ModelViewSet):
    serializer_class = LoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LoteFilter
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [Authenticated]
        else:
            permission_classes = [Producao | Admin]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.cargo == 'Admin':
            return Lote.objects.all()
        
        if user.cargo == 'Inspecao':
            return Lote.objects.filter(
                Q(status_inspecao__isnull=True) | Q(responsavel=user)
            )
        
        if user.cargo in ['Engenharia', 'Producao']:
            return Lote.objects.all()
        
        return Lote.objects.none()

    @action(detail=False, methods=['get'], permission_classes=[LiderProducao | Admin])
    def dashboard(self, request):
        dt_inicio = request.query_params.get('dt_inicio', None)
        dt_fim = request.query_params.get('dt_fim', None)
        funcionario_id = request.query_params.get('funcionario_id', None)
        
        itens = Item.objects.all()
        
        if dt_inicio and dt_fim:
            itens = itens.filter(dthItem__gte=dt_inicio, dthItem__lte=dt_fim)
        
        if funcionario_id:
            itens = itens.filter(lote__responsavel_inspecao_id=funcionario_id)
        
        total_aprovados = itens.filter(lote__status_inspecao='Aprovado').count()
        total_reprovados = itens.filter(lote__status_inspecao='Reprovado').count()
        
        return Response({
            'total_pecas_aprovadas': total_aprovados,
            'total_pecas_reprovadas': total_reprovados,
            'total_pecas': itens.count()
        })