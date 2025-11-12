from .__init__ import *
from ..serializers.customuser import FuncionarioNomeSerializer

class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioNomeSerializer
    permission_classes = [permissions.IsAdminUser]