from rest_framework import serializers
from .models import Categoria, Funcionario, Veiculo, Viagem, Manutencao

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = '__all__'


class VeiculoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)

    class Meta:
        model = Veiculo
        fields = '__all__'


class ViagemSerializer(serializers.ModelSerializer):
    motorista_nome = serializers.CharField(source='motorista.nome', read_only=True)
    veiculo_modelo = serializers.CharField(source='veiculo.modelo', read_only=True)

    class Meta:
        model = Viagem
        fields = '__all__'


class ManutencaoSerializer(serializers.ModelSerializer):
    veiculo_placa = serializers.CharField(source='veiculo.num_placa', read_only=True)
    funcionario_nome = serializers.CharField(source='funcionario.nome', read_only=True)

    class Meta:
        model = Manutencao
        fields = '__all__'
