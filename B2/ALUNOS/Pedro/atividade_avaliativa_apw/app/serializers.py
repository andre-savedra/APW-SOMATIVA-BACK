from rest_framework import serializers
from .models import Produto, Funcionario, Maquina, Manutencao, Lote, Producao

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = '__all__'

class ManutencaoSerializer(serializers.ModelSerializer):
    encarregado = FuncionarioSerializer(read_only=True)

    class Meta:
        model = Manutencao
        fields = ['id', 'data_hora', 'descricao', 'encarregado']

class MaquinaSerializer(serializers.ModelSerializer):
    historico = ManutencaoSerializer(many=True, read_only=True)

    class Meta:
        model = Maquina
        fields = ['id', 'codigo', 'foto', 'descricao', 'historico']

class LoteSerializer(serializers.ModelSerializer):
    produtos = ProdutoSerializer(many=True, read_only=True)
    maquina = MaquinaSerializer(read_only=True)
    encarregado_inspecao = FuncionarioSerializer(read_only=True)

    class Meta:
        model = Lote
        fields = [
            'id', 'codigo', 'data_inicio', 'data_final', 'data_inspecao',
            'status_inspecao', 'produtos', 'maquina', 'encarregado_inspecao', 'qrcode'
        ]

class ProducaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producao
        fields = '__all__'
