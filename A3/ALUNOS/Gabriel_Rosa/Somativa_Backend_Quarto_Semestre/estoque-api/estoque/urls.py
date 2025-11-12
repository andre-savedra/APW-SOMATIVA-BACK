from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'marcas', views.MarcaViewSet)
router.register(r'setores', views.SetorViewSet)
router.register(r'produtos', views.ProdutoViewSet)
router.register(r'escaninhos', views.EscaninhoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]