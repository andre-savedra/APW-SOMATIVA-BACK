from rest_framework import serializers
from .models import Categoria, Marca, Produto, Setor, Escaninho


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'data_registro']
        read_only_fields = ['data_registro']


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['id', 'nome', 'cnpj', 'data_inclusao']
        read_only_fields = ['data_inclusao']


class ProdutoListSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    marca = MarcaSerializer(read_only=True)
    
    class Meta:
        model = Produto
        fields = [
            'id', 'nome', 'codigo_registro', 'codigo_barras',
            'categoria', 'marca', 'data_cadastro', 'custo',
            'valor_venda', 'informacoes_adicionais', 'em_promocao'
        ]


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = [
            'id', 'nome', 'codigo_registro', 'codigo_barras',
            'categoria', 'marca', 'data_cadastro', 'custo',
            'valor_venda', 'informacoes_adicionais', 'em_promocao'
        ]
        read_only_fields = ['data_cadastro']


class EscaninhoListSerializer(serializers.ModelSerializer):
    produto = ProdutoListSerializer(read_only=True)
    setor_letra = serializers.CharField(source='setor.letra', read_only=True)
    
    class Meta:
        model = Escaninho
        fields = ['id', 'codigo', 'setor', 'setor_letra', 'produto', 'quantidade']


class EscaninhoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escaninho
        fields = ['id', 'codigo', 'setor', 'produto', 'quantidade']


class SetorListSerializer(serializers.ModelSerializer):
    escaninhos = EscaninhoListSerializer(many=True, read_only=True)
    
    class Meta:
        model = Setor
        fields = ['id', 'letra', 'descricao', 'data_cadastro', 'escaninhos']


class SetorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setor
        fields = ['id', 'letra', 'descricao', 'data_cadastro']
        read_only_fields = ['data_cadastro']