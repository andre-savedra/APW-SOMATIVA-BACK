from rest_framework import serializers
from ..models.maquinas import Maquina

class MaquinaSerializer(serializers.ModelSerializer):
    responsavel_manutencao_nome = serializers.CharField(source='responsavel_manutencao.nome', read_only=True)
    class Meta:
        model = Maquina
        fields = '__all__'
        read_only_fields = ['precisa_manutencao']