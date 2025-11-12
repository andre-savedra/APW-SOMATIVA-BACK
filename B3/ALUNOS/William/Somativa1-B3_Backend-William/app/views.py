from . import models
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateFromToRangeFilter, ChoiceFilter, CharFilter
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

from .models import Guest, Accommodation, Reservation, Employee, CleaningRecord, MaintenanceRecord
from .serializers import (GuestSerializer, AccommodationSerializer, ReservationSerializer,
                          EmployeeSerializer, CleaningRecordSerializer, MaintenanceRecordSerializer)
from .permissions import IsReceptionCreateEditView, IsGovernanceOnlyCleaning, IsMaintenance

# ===============================
# Filters for Reservation
# ===============================
class ReservationFilter(FilterSet):
    data_checkin = DateFromToRangeFilter(field_name='data_checkin')
    data_checkout = DateFromToRangeFilter(field_name='data_checkout')
    status = ChoiceFilter(field_name='status', choices=Reservation.STATUS_CHOICES)
    tipo_acomodacao = CharFilter(field_name='acomodacao__tipo')
    nacionalidade = CharFilter(field_name='hospede__nacionalidade')

    class Meta:
        model = Reservation
        fields = ['data_checkin', 'data_checkout', 'status', 'tipo_acomodacao', 'nacionalidade']


# ===============================
# Guest ViewSet
# ===============================
class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['nome_completo','cpf','email']


# ===============================
# Accommodation ViewSet
# ===============================
class AccommodationViewSet(viewsets.ModelViewSet):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['numero','tipo','status']

    @action(
        detail=False,
        methods=['get'],
        url_path='not-cleaned-7days',
        permission_classes=[IsGovernanceOnlyCleaning]
    )
    def not_cleaned_7days(self, request):
        cutoff = timezone.now().date() - timedelta(days=7)
        acoms = Accommodation.objects.filter(
            Q(data_ultima_limpeza__lt=cutoff) | Q(data_ultima_limpeza__isnull=True)
        )
        page = self.paginate_queryset(acoms)
        serializer = self.get_serializer(page or acoms, many=True)
        return self.get_paginated_response(serializer.data) if page is not None else Response(serializer.data)


# ===============================
# Reservation ViewSet
# ===============================
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().select_related('hospede','acomodacao')
    serializer_class = ReservationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ReservationFilter
    search_fields = ['codigo','hospede__nome_completo','acomodacao__numero']
    permission_classes = [IsReceptionCreateEditView]  # Recepção só cria/edita, não exclui

    def destroy(self, request, *args, **kwargs):
        # Deletion blocked for reception-level users (permission layer ensures this)
        return super().destroy(request, *args, **kwargs)


# ===============================
# Employee ViewSet
# ===============================
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome','matricula','cargo']


# ===============================
# CleaningRecord ViewSet
# ===============================
class CleaningRecordViewSet(viewsets.ModelViewSet):
    queryset = CleaningRecord.objects.all().select_related('funcionario','acomodacao')
    serializer_class = CleaningRecordSerializer
    permission_classes = [IsGovernanceOnlyCleaning]

    def create(self, request, *args, **kwargs):
        # Ao criar registro de limpeza, atualizar a data_ultima_limpeza da acomodação
        resp = super().create(request, *args, **kwargs)
        data = resp.data
        acom_id = data.get('acomodacao')
        data_limpeza = data.get('data_limpeza')
        if acom_id and data_limpeza:
            Accommodation.objects.filter(pk=acom_id).update(data_ultima_limpeza=data_limpeza)
        return resp


# ===============================
# MaintenanceRecord ViewSet
# ===============================
class MaintenanceRecordViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRecord.objects.all().select_related('funcionario','acomodacao')
    serializer_class = MaintenanceRecordSerializer
    permission_classes = [IsMaintenance]

    def create(self, request, *args, **kwargs):
        # Ao criar manutenção, opcional: atualizar status da acomodação se enviado
        status_acomodacao = request.data.get('status_acomodacao')
        acom_id = request.data.get('acomodacao')
        resp = super().create(request, *args, **kwargs)
        if acom_id and status_acomodacao:
            Accommodation.objects.filter(pk=acom_id).update(status=status_acomodacao)
        return resp
