from .views import *
from rest_framework.routers import DefaultRouter
from django.contrib import admin

router = DefaultRouter()

router.register(r'produto',ProdutoView)
router.register(r'pedido',PedidoView)
router.register(r'users', CustomUserView)


urlpatterns = router.urls