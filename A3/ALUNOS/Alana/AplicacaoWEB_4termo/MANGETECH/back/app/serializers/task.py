from rest_framework import serializers
from ..models import *

#LEMBRANDO: serializers serve para transformar Json em python e vice versa

class TaskReadSerializer(serializers.ModelSerializer):
    from .custom_user import CustomUserSerializer
    from .equipment import EquipmentSerializer
    creator_FK = CustomUserSerializer() #puxa as informações do usuario
    equipments_FK = EquipmentSerializer(many=True) #puxa as informações do equipamento
    responsibles_FK = CustomUserSerializer(many=True)
    
    class Meta:
        model = Task
        fields = '__all__'
        many= True

class TaskWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        many= True
