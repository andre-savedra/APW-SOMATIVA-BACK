from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    UserView, CategoryView, ProductView, MachineView,
    LoteView, MaintenceView, RegisterAPIView, LoginAPIView,
    DashboardView
)

router = DefaultRouter()
router.register(r'users', UserView, basename='user')
router.register(r'categories', CategoryView, basename='category')
router.register(r'products', ProductView, basename='product')
router.register(r'machines', MachineView, basename='machine')
router.register(r'lotes', LoteView, basename='lote')
router.register(r'maintences', MaintenceView, basename='maintence')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
]