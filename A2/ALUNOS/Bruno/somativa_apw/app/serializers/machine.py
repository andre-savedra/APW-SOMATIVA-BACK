from rest_framework import serializers
from ..models import Machine
from ..serializers.custom_user import CustomUserSerializer
from .machine_maintenance import MachineMaintenanceSerializer

class MachineWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'
        many= True

# Serializer de Leitura 
class MachineReadSerializer(serializers.ModelSerializer):
    maintenance_history = MachineMaintenanceSerializer(
        many=True, 
        read_only=True, 
        source='MachineMaintenance_machine_FK' # Usa o related_name do ForeignKey
    ) 

    class Meta:
        model = Machine     
        fields = [
            'id', 
            'code',
            'description',
            'photo',
            'maintenance_history' 
        ]