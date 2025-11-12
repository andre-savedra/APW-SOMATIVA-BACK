from django.contrib import admin
from django.urls import path, include

# imports p endpoints de token jwt:
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # rota principal da api:
    path('api/', include('app.urls')),
    
    # rotas de autenticação:
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]