from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (GuestViewSet, AccommodationViewSet, ReservationViewSet,
                    EmployeeViewSet, CleaningRecordViewSet, MaintenanceRecordViewSet)

router = DefaultRouter()
router.register(r'hospedes', GuestViewSet)
router.register(r'acomodacoes', AccommodationViewSet)
router.register(r'reservas', ReservationViewSet)
router.register(r'funcionarios', EmployeeViewSet)
router.register(r'limpezas', CleaningRecordViewSet)
router.register(r'manutencoes', MaintenanceRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
