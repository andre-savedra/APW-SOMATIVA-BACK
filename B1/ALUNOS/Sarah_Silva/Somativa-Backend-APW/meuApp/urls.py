from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.employee import EmployeeView
from .views.maintenance import MaintenanceView
from .views.trip import TripView
from .views.vehicle import VehicleView

router = DefaultRouter()

router.register(r'employee', EmployeeView)
router.register(r'maintenance', MaintenanceView)
router.register(r'trip', TripView)
router.register(r'vehicle', VehicleView)


urlpatterns = [
    path('', include(router.urls)),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
