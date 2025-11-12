from rest_framework import serializers
from ..models.sector import Setor
from .shelf import EscaninhoSerializer

class SetorSerializer(serializers.ModelSerializer):
    escaninhos = EscaninhoSerializer(many=True, read_only=True)

    class Meta:
        model = Setor
        fields = '__all__'