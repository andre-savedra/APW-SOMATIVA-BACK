
from django.urls import path, include
from rest_framework import routers
from .views import (
    UserViewSet, ProdutoViewSet, LoteViewSet,
    MaquinaViewSet, ManutencaoViewSet, ItemProduzidoViewSet,
    DashboardViewSet
)

router = routers.DefaultRouter()
router.register(r'usuarios', UserViewSet)
router.register(r'produtos', ProdutoViewSet)
router.register(r'lotes', LoteViewSet)
router.register(r'maquinas', MaquinaViewSet)
router.register(r'manutencoes', ManutencaoViewSet)
router.register(r'itens', ItemProduzidoViewSet)
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
]