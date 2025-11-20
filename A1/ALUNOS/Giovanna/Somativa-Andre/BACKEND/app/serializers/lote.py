from rest_framework import serializers
from ..models import Lote

class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = '__all__'

class LoteReadSerializer(serializers.ModelSerializer):
    funcionario_nome = serializers.CharField(source='funcionario_FK.username', read_only=True)
    produto_nome = serializers.CharField(source='produto_FK.nome', read_only=True)
    
    class Meta:
        model = Lote
        fields = '__all__'

class LoteWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = '__all__'


