from rest_framework import serializers
from ..models.machine import MachineMaintenance
from ..serializers.custom_user import CustomUserSerializer
from ..serializers.product import ProductSerializer

class MachineMaintenanceSerializer(serializers.ModelSerializer):
    user_FK = CustomUserSerializer(read_only=True)
    product_FK = ProductSerializer(read_only=True)

    class Meta:
        model = MachineMaintenance
        fields = '__all__'
        many= True