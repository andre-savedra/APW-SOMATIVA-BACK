from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        'message': 'API de Estoque - Sistema de Gerenciamento',
        'version': '1.0.0',
        'endpoints': {
            'auth': {
                'token': '/api/auth/token/',
                'refresh': '/api/auth/refresh/',
                'verify': '/api/auth/verify/',
            },
            'resources': {
                'categorias': '/api/categorias/',
                'marcas': '/api/marcas/',
                'setores': '/api/setores/',
                'produtos': '/api/produtos/',
                'escaninhos': '/api/escaninhos/',
            },
            'special_endpoints': {
                'produtos_mais_antigos': '/api/produtos/mais-antigos/',
                'produtos_promocao': '/api/produtos/em-promocao/',
                'buscar_codigo_barras': '/api/produtos/buscar-codigo-barras/?codigo=123',
                'escaninhos_com_produtos': '/api/escaninhos/com-produtos/',
                'escaninhos_vazios': '/api/escaninhos/vazios/',
            }
        },
        'admin': '/admin/',
        'docs': 'https://github.com/seu-usuario/estoque-api'
    })

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Root
    path('api/', api_root, name='api-root'),
    
    # Authentication
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # API Endpoints
    path('api/', include('estoque.urls')),
]