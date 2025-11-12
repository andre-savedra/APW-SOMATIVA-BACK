from rest_framework import serializers
from ..models import *

class ProducaoSerializer(serializers.ModelSerializer):
        class Meta:
                model = Producao
                fields = '__all__'
                many= True