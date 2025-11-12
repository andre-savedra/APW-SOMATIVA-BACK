from rest_framework import serializers
from ..models.shelf import Escaninho

class EscaninhoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escaninho
        fields = '__all__'