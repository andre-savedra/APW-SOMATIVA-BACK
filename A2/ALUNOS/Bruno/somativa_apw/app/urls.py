from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'custom-user',CustomUserView)
router.register(r'category',CategoryView)
router.register(r'product', ProductView)
router.register(r'machine',MachineView)
router.register(r'machine-maintenance', MachineMaintenanceView)
router.register(r'lot',LotView)
router.register(r'item',ItemView)

urlpatterns = router.urls