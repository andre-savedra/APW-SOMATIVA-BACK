from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet,
    ProdutoViewSet,
    FuncionarioViewSet,
    MaquinaViewSet,
    ManutencaoViewSet,
    LoteViewSet,
    ItemProducaoViewSet,
    DashboardView,
)

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'produtos', ProdutoViewSet)
router.register(r'funcionarios', FuncionarioViewSet)
router.register(r'maquinas', MaquinaViewSet)
router.register(r'manutencoes', ManutencaoViewSet)
router.register(r'lotes', LoteViewSet)
router.register(r'itens', ItemProducaoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]

