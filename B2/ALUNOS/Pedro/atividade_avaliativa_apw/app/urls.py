from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FuncionarioViewSet, ProducaoViewSet, LoteViewSet, MaquinaViewSet, ProdutoViewSet

router = DefaultRouter()
router.register(r'funcionarios', FuncionarioViewSet)
router.register(r'producao', ProducaoViewSet)
router.register(r'lotes', LoteViewSet)
router.register(r'maquinas', MaquinaViewSet)
router.register(r'produtos', ProdutoViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
