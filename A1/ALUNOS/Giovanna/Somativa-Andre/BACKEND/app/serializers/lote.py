from rest_framework import serializers
from ..models import *

class LoteSerializer(serializers.ModelSerializer):
        class Meta:
                model = Lote
                fields = '__all__'
                many= True