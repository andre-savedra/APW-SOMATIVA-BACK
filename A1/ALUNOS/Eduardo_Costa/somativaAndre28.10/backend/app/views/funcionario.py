from rest_framework.viewsets import ModelViewSet
from ..models import *
from ..serializers import *
from ..permissions import *

class FuncionarioView(ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
    permission_classes = [Admin]
