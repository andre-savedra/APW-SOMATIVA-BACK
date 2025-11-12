from rest_framework.routers import DefaultRouter
from .views.customuser import FuncionarioViewSet
from .views.produtos import CategoriaViewSet, ProdutoViewSet
from .views.maquinas import MaquinaViewSet
from .views.lote import LoteViewSet
from .views.itemproducao import ItemProducaoViewSet
from .views.manutencao import ManutencaoViewSet

router = DefaultRouter()
router.register(r'funcionarios', FuncionarioViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'produtos', ProdutoViewSet)
router.register(r'maquinas', MaquinaViewSet)
router.register(r'lotes', LoteViewSet, basename='lote')
router.register(r'itens-producao', ItemProducaoViewSet)
router.register(r'manutencao', ManutencaoViewSet)

urlpatterns = router.urls