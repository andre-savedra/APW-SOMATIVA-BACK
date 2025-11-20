from rest_framework.viewsets import ModelViewSet
from ..models import Categoria
from ..serializers import CategoriaSerializer
from rest_framework.response import Response
from rest_framework import status

def is_Engenharia(user):
    return hasattr(user, 'cargo') and user.cargo == 'ENGENHARIA'

def is_Admin(user):
    return user.is_superuser

class CategoriaView(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Você não está autenticado!"}, status=status.HTTP_403_FORBIDDEN)
        if not (is_Engenharia(request.user) or is_Admin(request.user)):
            return Response({"detail": "Apenas Engenharia ou Admin podem criar categorias."}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Você não está autenticado!"}, status=status.HTTP_403_FORBIDDEN)
        if not (is_Engenharia(request.user) or is_Admin(request.user)):
            return Response({"detail": "Apenas Engenharia ou Admin podem editar categorias."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
