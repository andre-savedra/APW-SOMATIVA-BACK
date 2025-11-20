from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'categoria', CategoriaView, basename='categoria')
router.register(r'produto', ProdutoView, basename='produto')
router.register(r'maquina', MaquinaView, basename='maquina')
router.register(r'funcionario', FuncionarioView, basename='funcionario')
router.register(r'lote', LoteView, basename='lote')
router.register(r'item', ItemView, basename='item')

urlpatterns = router.urls