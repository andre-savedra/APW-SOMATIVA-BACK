from rest_framework import serializers
from .models import Categoria, Marca, Setor, Produto, Escaninho

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'

class SetorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setor
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
    # mostrar os dados detalhados
    categoria = CategoriaSerializer(read_only=True)
    marca = MarcaSerializer(read_only=True)
    
    # criar e atualizar apenas cm o id:
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), source='categoria', write_only=True
    )
    marca_id = serializers.PrimaryKeyRelatedField(
        queryset=Marca.objects.all(), source='marca', write_only=True
    )

    class Meta:
        model = Produto
        fields = [
            'id', 'nome', 'codigo_barras_numerico', 'data_cadastro', 'custo', 
            'valor_venda', 'informacoes_adicionais', 'em_promocao',
            'categoria', 'marca', 'categoria_id', 'marca_id'
        ]

class EscaninhoSerializer(serializers.ModelSerializer):
    setor = SetorSerializer(read_only=True)
    produto = ProdutoSerializer(read_only=True) 

    setor_id = serializers.PrimaryKeyRelatedField(
        queryset=Setor.objects.all(), source='setor', write_only=True
    )
    produto_id = serializers.PrimaryKeyRelatedField(
        queryset=Produto.objects.all(), source='produto', write_only=True, allow_null=True
    )

    class Meta:
        model = Escaninho
        fields = [
            'id', 'codigo_escaninho', 'localizacao', 'quantidade',
            'setor', 'produto', 'setor_id', 'produto_id'
        ]