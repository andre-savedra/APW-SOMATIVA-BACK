from rest_framework import serializers
from ..models import Escaninhos

class EscaninhosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escaninhos
        fields = '__all__'
        many= True