from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Categoria,
    Produto,
    Funcionario,
    Maquina,
    Manutencao,
    Lote,
    ItemProducao,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome']


class ProdutoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)

    class Meta:
        model = Produto
        fields = ['id', 'nome', 'codigo', 'descricao', 'categoria', 'categoria_nome']


class FuncionarioSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )

    class Meta:
        model = Funcionario
        fields = [
            'id', 'user', 'user_id', 'nome', 'registro', 'email', 'cpf', 'data_contratacao', 'cargo'
        ]


class MaquinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maquina
        fields = ['id', 'codigo', 'foto', 'nome', 'descricao']


class ManutencaoSerializer(serializers.ModelSerializer):
    funcionario_nome = serializers.CharField(source='funcionario.nome', read_only=True)

    class Meta:
        model = Manutencao
        fields = ['id', 'maquina', 'data_hora', 'descricao', 'funcionario', 'funcionario_nome']


class ItemProducaoSerializer(serializers.ModelSerializer):
    maquina_codigo = serializers.CharField(source='maquina.codigo', read_only=True)

    class Meta:
        model = ItemProducao
        fields = ['id', 'lote', 'data_hora', 'maquina', 'maquina_codigo']


class LoteSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    categoria_nome = serializers.CharField(source='produto.categoria.nome', read_only=True)
    inspetor_nome = serializers.CharField(source='inspetor.nome', read_only=True)
    itens = ItemProducaoSerializer(many=True, read_only=True)

    class Meta:
        model = Lote
        fields = [
            'id', 'codigo', 'produto', 'produto_nome', 'categoria_nome',
            'inicio', 'fim', 'data_inspecao', 'inspetor', 'inspetor_nome', 'status_inspecao', 'itens'
        ]

