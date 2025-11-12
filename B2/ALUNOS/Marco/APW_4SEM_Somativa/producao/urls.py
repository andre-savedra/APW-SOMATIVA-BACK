from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    FuncionarioViewSet, LinhaViewSet, OrdemProducaoViewSet,
    RegistroViewSet, AlertaViewSet, ManutencaoViewSet
)

router = DefaultRouter()
router.register(r'funcionarios', FuncionarioViewSet)
router.register(r'linhas', LinhaViewSet)
router.register(r'ordens-producao', OrdemProducaoViewSet)
router.register(r'registros', RegistroViewSet)
router.register(r'alertas', AlertaViewSet)
router.register(r'manutencoes', ManutencaoViewSet)
from .views import ProdutoViewSet, MaquinaViewSet, ManutencaoMaquinaViewSet, LoteViewSet, ItemProducaoViewSet
router.register(r'produtos', ProdutoViewSet)
router.register(r'maquinas', MaquinaViewSet)
router.register(r'manutencoes-maquina', ManutencaoMaquinaViewSet)
router.register(r'lotes', LoteViewSet)
router.register(r'itens-producao', ItemProducaoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]