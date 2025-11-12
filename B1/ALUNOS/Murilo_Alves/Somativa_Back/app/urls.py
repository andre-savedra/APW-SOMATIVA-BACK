from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FuncionarioViewSet, VeiculoViewSet, ViagemViewSet, ManutencaoViewSet

router = DefaultRouter()
router.register(r'funcionarios', FuncionarioViewSet)
router.register(r'veiculos', VeiculoViewSet)
router.register(r'viagens', ViagemViewSet)
router.register(r'manutencoes', ManutencaoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
