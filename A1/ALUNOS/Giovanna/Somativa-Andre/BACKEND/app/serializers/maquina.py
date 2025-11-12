from rest_framework import serializers
from ..models import *

class MaquinaSerializer(serializers.ModelSerializer):
        class Meta:
                model = Maquina
                fields = '__all__'
                many= True