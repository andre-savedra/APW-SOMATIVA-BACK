from rest_framework import serializers
from .models import *

class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'

class FuncionarioSerializer(serializers.ModelSerializer):
    cargo_nome = serializers.CharField(source='cargo.nome', read_only=True)
    class Meta:
        model = Funcionario
        fields = '__all__'

class MaquinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maquina
        fields = '__all__'

class ManutencaoSerializer(serializers.ModelSerializer):
    funcionario_nome = serializers.CharField(source='funcionario.nome', read_only=True)
    class Meta:
        model = Manutencao
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

# --- Itens do Lote detalhados ---
class ItemLoteSerializer(serializers.ModelSerializer):
    maquina_nome = serializers.CharField(source='maquina.nome', read_only=True)
    maquina_codigo = serializers.CharField(source='maquina.codigo', read_only=True)
    maquina_descricao = serializers.CharField(source='maquina.descricao', read_only=True)
    
    class Meta:
        model = ItemLote
        fields = [
            'id',
            'lote',
            'data_hora',
            'maquina',
            'maquina_nome',
            'maquina_codigo',
            'maquina_descricao'
        ]

# --- Lotes com todos os detalhes ---
class LoteSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    produto_categoria = serializers.CharField(source='produto.categoria', read_only=True)
    responsavel_nome = serializers.CharField(source='responsavel_inspecao.nome', read_only=True)
    responsavel_cargo = serializers.CharField(source='responsavel_inspecao.cargo.nome', read_only=True)
    itens = ItemLoteSerializer(many=True, read_only=True)

    class Meta:
        model = Lote
        fields = [
            'id',
            'codigo',
            'produto',
            'produto_nome',
            'produto_categoria',
            'data_inicio',
            'data_fim',
            'data_inspecao',
            'status_inspecao',
            'responsavel_inspecao',
            'responsavel_nome',
            'responsavel_cargo',
            'itens'
        ]

