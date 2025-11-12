from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateFromToRangeFilter, CharFilter
from .models import Hospede, Acomodacao, Reserva, Manutencao
from .serializers import (HospedeSerializer, AcomodacaoSerializer,
                          ReservaListSerializer, ReservaDetailSerializer, ReservaCreateUpdateSerializer,
                          ManutencaoSerializer)
from .permissions import IsReceptionCreateEdit, IsGovernanca, IsManutencao
from django.utils import timezone
from datetime import timedelta
from django.db import models

# Create your views here.
class ReservaFilter(FilterSet):
    check_in = DateFromToRangeFilter(field_name='check_in')
    check_out = DateFromToRangeFilter(field_name='check_out')
    status = CharFilter(field_name='status')
    tipo_acomodacao = CharFilter(method='filter_tipo_acomodacao')
    nacionalidade_hospede = CharFilter(field_name='hospede__nacionalidade')

    class Meta:
        model = Reserva
        fields = ['status','check_in','check_out','hospede__nacionalidade']

    def filter_tipo_acomodacao(self, queryset, name, value):
        return queryset.filter(acomodacao__tipo__iexact=value)

class HospedeViewSet(viewsets.ModelViewSet):
    queryset = Hospede.objects.all()
    serializer_class = HospedeSerializer
    filter_backends = [DjangoFilterBackend]

class AcomodacaoViewSet(viewsets.ModelViewSet):
    queryset = Acomodacao.objects.select_related('funcionario_responsavel').all()
    serializer_class = AcomodacaoSerializer
    filter_backends = [DjangoFilterBackend]

    @action(detail=False, methods=['get'], url_path='sujo-mais-7dias')
    def sujas_mais_7dias(self, request):
        sete_dias_atras = timezone.now().date() - timedelta(days=7)
        q = self.get_queryset().filter(models.Q(data_ultima_limpeza__lt=sete_dias_atras) | models.Q(data_ultima_limpeza__isnull=True))
        serializer = self.get_serializer(q, many=True)
        return Response(serializer.data)

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.select_related('hospede','acomodacao').all()
    filterset_class = ReservaFilter
    filter_backends = [DjangoFilterBackend]
    ordering_fields = ['check_in','check_out','valor_total']
    search_fields = ['codigo','hospede__nome_completo','acomodacao__numero']

    def get_serializer_class(self):
        if self.action == 'list':
            return ReservaListSerializer
        if self.action in ['retrieve']:
            return ReservaDetailSerializer
        return ReservaCreateUpdateSerializer

    def get_permissions(self):
        # Define permissões por ação:
        if self.action in ['create','update','partial_update']:
            return [IsReceptionCreateEdit()]
        if self.action == 'destroy':
            from rest_framework.permissions import IsAdminUser
            return [IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)

class ManutencaoViewSet(viewsets.ModelViewSet):
    queryset = Manutencao.objects.select_related('acomodacao','realizado_por').all()
    serializer_class = ManutencaoSerializer

    def get_permissions(self):
        if self.action in ['create','update','partial_update']:
            return [IsManutencao()]
        return [permissions.IsAuthenticated()]
