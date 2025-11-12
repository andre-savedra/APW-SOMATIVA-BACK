from rest_framework import serializers
from .models import Funcionario, Veiculo, Viagem, Manutencao, CategoriaVeiculo # 

class CategoriaVeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaVeiculo
        fields = '__all__'



class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = '__all__'

class VeiculoNestedSerializer(serializers.ModelSerializer):
    categoria = serializers.StringRelatedField()

    class Meta:
        model = Veiculo
        fields = ['id', 'placa', 'modelo', 'categoria']

class VeiculoSerializer(serializers.ModelSerializer):

    categoria_detalhes = CategoriaVeiculoSerializer(source='categoria', read_only=True)

    class Meta:
        model = Veiculo
        fields = [
            'id', 'placa', 'modelo', 'data_aquisicao', 'data_ultima_manutencao',
            'categoria',
            'categoria_detalhes' 
        ]
        extra_kwargs = {
            'categoria': {'write_only': True}
        }


class ViagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viagem
        fields = '__all__'


class ManutencaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manutencao
        fields = '__all__'