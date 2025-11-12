from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    CategoriaViewSet, MarcaViewSet, ProdutoViewSet,
    SetorViewSet, EscaninhoViewSet
)

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'marcas', MarcaViewSet, basename='marca')
router.register(r'produtos', ProdutoViewSet, basename='produto')
router.register(r'setores', SetorViewSet, basename='setor')
router.register(r'escaninhos', EscaninhoViewSet, basename='escaninho')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]