from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Criar router e registrar ViewSets
router = DefaultRouter()
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'marcas', views.MarcaViewSet)
router.register(r'setores', views.SetorViewSet)
router.register(r'produtos', views.ProdutoViewSet)
router.register(r'escaninhos', views.EscaninhoViewSet)
router.register(r'usuarios', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]