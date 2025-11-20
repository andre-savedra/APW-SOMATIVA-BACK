from rest_framework.viewsets import ModelViewSet
from ..models import *
from ..serializers import *
from rest_framework.response import Response
from ..serializers import ProdutoSerializer
from ..utils import is_Engenharia, is_Admin
from rest_framework.response import Response
from rest_framework import status

class ProdutoView(ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        if not (is_Engenharia(user) or is_Admin(user)):
            return Response(
                {"detail": "Apenas engenharia ou admin podem criar produtos."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)
