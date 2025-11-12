from rest_framework import serializers
from ..models.manutencao import Manutencao

class ManutencaoSerializer(serializers.ModelSerializer):
    responsavel_nome = serializers.CharField(source='responsavel.nome', read_only=True)
    maquina_nome = serializers.CharField(source='maquina.nome', read_only=True)
    
    class Meta:
        model = Manutencao
        fields = '__all__'
        read_only_fields = ['data_manutencao']