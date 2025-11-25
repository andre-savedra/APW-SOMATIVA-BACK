from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'funcionarios', FuncionarioViewSet, basename='funcionario')
router.register(r'produtos', ProdutoViewSet, basename='produto')
router.register(r'maquinas', MaquinaViewSet, basename='maquina')
router.register(r'manutencoes', ManutencaoViewSet, basename='manutencao')
router.register(r'lotes', LoteViewSet, basename='lote')
router.register(r'itens-producao', ItemProducaoViewSet, basename='item-producao')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')
router.register(r'maquinas-manutencao', MaquinaManutencaoViewSet, basename='maquina-manutencao')  # ⭐ ADICIONE ESTA LINHA

urlpatterns = [
    path('', include(router.urls)),
]
