from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'customuser', CustomUserView)
router.register(r'ambiente',AmbienteView)
router.register(r'ativo',AtivoView)
router.register(r'tarefas',TarefasView)
router.register(r'historicostatus',HistoricoStatusView)
router.register(r'tarefas/status',TarefaStatusImageView)
router.register(r'notification',NotificationView)
router.register(r'category',CategoryView)


urlpatterns = router.urls