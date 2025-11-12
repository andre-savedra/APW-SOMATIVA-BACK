from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MaintenanceHistoryViewSet,
    CustomUserViewSet,
    GuestViewSet,
    EmployeeViewSet,
    AccommodationViewSet,
    ReservationViewSet,
)

router = DefaultRouter()
router.register(r'guests', GuestViewSet, basename='guest')
router.register(r'custom_user', CustomUserViewSet, basename='custom_user')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'accommodation', AccommodationViewSet, basename='accommodation')
router.register(r'reservation', ReservationViewSet, basename='reservation')
router.register(r'maintenance-history', MaintenanceHistoryViewSet, basename='maintenancehistory')

urlpatterns = [
    path('', include(router.urls)),
]




