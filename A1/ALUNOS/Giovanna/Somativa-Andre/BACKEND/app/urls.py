from .views import *
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'categorias', CategoriaView, basename='categoria')
router.register(r'produtos', ProdutoView, basename='produto')
router.register(r'maquinas', MaquinaView, basename='maquina')
router.register(r'lotes', LoteView, basename='lote')
router.register(r'producoes', ProducaoView, basename='producao')
router.register(r'users', CustomUserView, basename='user')

urlpatterns = router.urls
