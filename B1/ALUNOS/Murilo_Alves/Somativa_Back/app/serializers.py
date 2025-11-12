from rest_framework import serializers
from .models import Funcionario, Veiculo, Viagem, Manutencao

# Nested serializers para que cada objeto traga seus relacionados

class ManutencaoSerializer(serializers.ModelSerializer):
    funcionario = serializers.StringRelatedField()  # nome do técnico
    veiculo = serializers.StringRelatedField()     # modelo do veículo

    class Meta:
        model = Manutencao
        fields = '__all__'


class ViagemSerializer(serializers.ModelSerializer):
    motorista = serializers.StringRelatedField()   # nome do motorista
    veiculo = serializers.StringRelatedField()     # modelo do veículo

    class Meta:
        model = Viagem
        fields = '__all__'


class VeiculoSerializer(serializers.ModelSerializer):
    manutencoes = ManutencaoSerializer(source='manutencao_set', many=True, read_only=True)
    viagens = ViagemSerializer(source='viagem_set', many=True, read_only=True)

    class Meta:
        model = Veiculo
        fields = '__all__'


class FuncionarioSerializer(serializers.ModelSerializer):
    manutencoes = ManutencaoSerializer(source='manutencao_set', many=True, read_only=True)
    viagens = ViagemSerializer(source='viagem_set', many=True, read_only=True)

    class Meta:
        model = Funcionario
        fields = '__all__'
