from rest_framework import serializers
from .models import *

class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = '__all__'


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'


class ManutencaoSerializer(serializers.ModelSerializer):
    funcionario_nome = serializers.CharField(source='funcionario.username', read_only=True)

    class Meta:
        model = Manutencao
        fields = '__all__'


class MaquinaSerializer(serializers.ModelSerializer):
    manutencoes = ManutencaoSerializer(many=True, read_only=True)

    class Meta:
        model = Maquina
        fields = '__all__'


class ItemProducaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemProducao
        fields = '__all__'


class LoteSerializer(serializers.ModelSerializer):
    itens = ItemProducaoSerializer(many=True, read_only=True)
    responsavel_nome = serializers.CharField(source='responsavel_inspecao.username', read_only=True)

    class Meta:
        model = Lote
        fields = '__all__'
