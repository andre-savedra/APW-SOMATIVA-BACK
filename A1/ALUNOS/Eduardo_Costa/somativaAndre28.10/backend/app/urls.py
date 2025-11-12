from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'funcionario',FuncionarioView)
router.register(r'maquina',MaquinaView)
router.register(r'item',ItemView)
router.register(r'lote',LoteView)
router.register(r'producao',ProducaoView)
router.register(r'produto',ProdutoView)

urlpatterns = router.urls