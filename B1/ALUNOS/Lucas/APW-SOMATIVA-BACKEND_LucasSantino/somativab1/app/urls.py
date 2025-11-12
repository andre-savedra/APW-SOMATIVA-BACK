from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet, FuncionarioViewSet, VeiculoViewSet,
    ViagemViewSet, ManutencaoViewSet, DashboardViewSet
)

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'funcionarios', FuncionarioViewSet)
router.register(r'veiculos', VeiculoViewSet)
router.register(r'viagens', ViagemViewSet)
router.register(r'manutencoes', ManutencaoViewSet)
router.register(r'dashboard', DashboardViewSet, basename='dashboard')


urlpatterns = [
    path('', include(router.urls)),
]
