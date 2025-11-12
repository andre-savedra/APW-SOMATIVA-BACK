from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'customuser', CustomUserViewSet)

router.register(r'produto', ProdutoView),
router.register(r'lote', LoteView),
router.register(r'itens', ItensLoteView),
router.register(r'maquina', MaquinaView),
router.register(r'manutencao', ManutencaoView),

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]