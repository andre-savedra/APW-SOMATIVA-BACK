from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import *


#2 Rotas (CRUDs)
router = DefaultRouter()
router.register(r'cargos', CargoView)
router.register(r'funcionarios', FuncionarioView)
router.register(r'maquinas', MaquinaView)
router.register(r'manutencoes', ManutencaoView)
router.register(r'produtos', ProdutoView)
router.register(r'lotes', LoteView)
router.register(r'itens', ItemLoteView)

#5 Rotas personalizadas
urlpatterns = [
    path('lotes/reprovados/', lotes_reprovados, name='lotes-reprovados'),  
    path('maquinas/precisam_manutencao/', maquinas_precisam_manutencao),
    path('dashboard/producao/', dashboard_producao),
]


# Junta tudo: router + rotas extras
urlpatterns += router.urls
