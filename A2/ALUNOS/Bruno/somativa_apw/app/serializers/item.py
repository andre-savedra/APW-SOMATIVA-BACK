from rest_framework import serializers
from ..models import Item
from ..serializers.lot import LotSerializer
from ..serializers.machine import MachineReadSerializer

class ItemSerializer(serializers.ModelSerializer):
    lot_FK = LotSerializer()
    machine_FK = MachineReadSerializer()

    class Meta:
        model = Item
        fields = ['id', 'lot_FK', 'machine_FK', 'date',]
        many= True