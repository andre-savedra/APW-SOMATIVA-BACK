from rest_framework import viewsets
from ..models.machine import Machine
from rest_framework import permissions
from ..serializers.machine import MachineReadSerializer, MachineWriteSerializer

class MachineView(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    permission_classes = [permissions.DjangoModelPermissions]

    # Escolhe o serializer correto com base na ação
    def get_serializer_class(self):
        # Se a ação for 'list' (ver a lista) ou 'retrieve' (ver um detalhe)
        if self.action in ['list', 'retrieve']:
            return MachineReadSerializer
        # Para qualquer outra ação ('create', 'update', 'partial_update')
        return MachineWriteSerializer
