from django.urls import path, include
from rest_framework import routers
from .views.equipment import ProdutoViewSet
from .views.category import CategoriaViewSet
from .views.brand import MarcaViewSet
from .views.shelf import EscaninhoViewSet
from .views.sector import SetorViewSet

router = routers.DefaultRouter()
router.register(r'produtos', ProdutoViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'marcas', MarcaViewSet)
router.register(r'escaninhos', EscaninhoViewSet)
router.register(r'setores', SetorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]