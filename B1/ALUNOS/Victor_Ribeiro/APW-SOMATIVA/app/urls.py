from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VeiculoViewSet, FuncionarioViewSet, ViagemViewSet, ManutencaoViewSet
from .views import UserCreateView, FuncionarioCreateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'veiculos', VeiculoViewSet)
router.register(r'funcionarios', FuncionarioViewSet)
router.register(r'viagens', ViagemViewSet)
router.register(r'manutencao', ManutencaoViewSet)

urlpatterns = [
    path('api/', include(router.urls)), 

        path('api/register-user/', UserCreateView.as_view(), name='register_user'),
    path('api/register-funcionario/', FuncionarioCreateView.as_view(), name='register_funcionario'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
]