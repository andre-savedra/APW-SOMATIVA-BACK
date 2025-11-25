from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *
from .views.maintenance import MachineNeedingMaintenanceView
from .views.dashboard import DashboardLeaderView

router = DefaultRouter()
router.register(r'custom-user',CustomUserView)
router.register(r'category',CategoryView)
router.register(r'product', ProductView)
router.register(r'machine',MachineView)
router.register(r'machine-maintenance', MachineMaintenanceView)
router.register(r'lot', LotView)
router.register(r'item',ItemView)

# Registra os endpoint protegidos com validação de grupo
urlpatterns = router.urls + [
    path(
        'maintenance-needed/', 
        MachineNeedingMaintenanceView.as_view(), 
        name='maintenance-needed'
    ),
    path(
        'dashboard/',
        DashboardLeaderView.as_view(),
        name='dashboard'
    )
]