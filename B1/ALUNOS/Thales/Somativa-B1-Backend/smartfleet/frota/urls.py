from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FuncionarioViewSet, 
    VeiculoViewSet, 
    ViagemViewSet, 
    ManutencaoViewSet,
    CategoriaVeiculoViewSet,
    DashboardView,
    VeiculosManutencaoAtrasadaView,
)

router = DefaultRouter()

router.register(r'funcionarios', FuncionarioViewSet, basename='funcionario')
router.register(r'veiculos', VeiculoViewSet, basename='veiculo')
router.register(r'viagens', ViagemViewSet, basename='viagem')
router.register(r'manutencoes', ManutencaoViewSet, basename='manutencao')
router.register(r'categorias-veiculos', CategoriaVeiculoViewSet, basename='categoria-veiculo')

urlpatterns = [

    path('', include(router.urls)),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path(
        'veiculos/manutencao-atrasada/', 
        VeiculosManutencaoAtrasadaView.as_view(), 
        name='veiculos-manutencao-atrasada'
    ),
]