from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum, Case, When, Count 
from django.db import models 


# ... restante do código do LoteViewSet ...
from django.utils import timezone
from datetime import timedelta

# Imports Modulares (Assumindo que os caminhos são os definidos no projeto)
from ..mixins import ReadWriteSerializerMixin
from ..models.lote import Lote
from ..models.itemproducao import ItemProducao 
from ..models.customuser import Cargo
from ..serializers.lote import LoteDetailSerializer, LoteSerializer
from ..filters.lote_filter import LoteFilter 
from ..permissions import LotePermission, IsLiderProducaoOrAdmin, get_user_cargo

REPROVADO_STATUS = 'REPROVADO'
PENDENTE_STATUS = 'PENDENTE'

class LoteViewSet(ReadWriteSerializerMixin, viewsets.ModelViewSet):
    
    # CORREÇÃO CRUCIAL: Define o QuerySet base para o Router (AssertionError)
    queryset = Lote.objects.all() 
    
    permission_classes = [LotePermission] 
    
    read_serializer_class = LoteDetailSerializer
    write_serializer_class = LoteSerializer
    
    filter_backends = [DjangoFilterBackend] 
    filterset_class = LoteFilter
    
    def get_queryset(self):
        user = self.request.user
        # O prefetch_related será aplicado em todos os casos de listagem
        queryset = self.queryset.prefetch_related('itens_produzidos')

        # --- REQUISITO 5: Lógica de Visualização para INSPEÇÃO ---
        if user.is_authenticated and user.cargo == Cargo.INSPECAO:
            queryset = queryset.filter(
                Q(status_inspecao=PENDENTE_STATUS) | Q(responsavel_inspecao=user)
            ).distinct()
        
        # --- REQUISITO 4: Lógica do Filtro 'reprovados=true' ---
        reprovados_only = self.request.query_params.get('reprovados', None)
        
        if reprovados_only and reprovados_only.lower() == 'true':
            # Filtra o status e aplica os filtros de data/máquina/categoria
            queryset = queryset.filter(status_inspecao=REPROVADO_STATUS)
            return self.filter_queryset(queryset)

        # Aplica o filtro padrão do DRF para todos os outros usuários/casos
        return self.filter_queryset(queryset)

    # --- REQUISITO 10: ENDPOINT DASHBOARD ---
    @action(detail=False, methods=['get'], permission_classes=[IsLiderProducaoOrAdmin])
    def dashboard(self, request):
        data_inicio_str = request.query_params.get('data_inicio')
        data_fim_str = request.query_params.get('data_fim')
        funcionario_id_str = request.query_params.get('funcionario_id')
        
        # O queryset inicial deve ser ItemProducao para contagem por peça
        queryset = ItemProducao.objects.all().select_related('lote', 'lote__responsavel_inspecao')
        
        # Filtros de data e funcionário
        if data_inicio_str:
            queryset = queryset.filter(data_hora_item__gte=data_inicio_str)
        if data_fim_str:
            queryset = queryset.filter(data_hora_item__lte=data_fim_str)
            
        if funcionario_id_str:
            queryset = queryset.filter(lote__responsavel_inspecao__id=funcionario_id_str)
            
        # Agregação (Contagem de peças por status de inspeção do Lote)
        dashboard_data = queryset.values('lote__status_inspecao').annotate(
            total_pecas=Count('lote__status_inspecao')
        ).order_by('lote__status_inspecao')
        
        response_data = {
            'total_pecas_aprovadas': 0,
            'total_pecas_reprovadas': 0,
            'total_pecas_pendentes': 0,
            'total_pecas_total': 0
        }
        
        for item in dashboard_data:
            status = item['lote__status_inspecao'].lower()
            total = item['total_pecas']
            
            if status == 'aprovado':
                response_data['total_pecas_aprovadas'] = total
            elif status == 'reprovado':
                response_data['total_pecas_reprovadas'] = total
            elif status == 'pendente':
                response_data['total_pecas_pendentes'] = total
            
            response_data['total_pecas_total'] += total
                
        return Response(response_data)