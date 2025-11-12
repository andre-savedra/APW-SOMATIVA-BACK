from rest_framework import serializers
from ..models.equipment import Produto
from .brand import MarcaSerializer
from .category import CategoriaSerializer

class ProdutoSerializer(serializers.ModelSerializer):
    marca = MarcaSerializer(read_only=True)
    categoria = CategoriaSerializer(read_only=True)

    class Meta:
        model = Produto
        fields = '__all__'