from rest_framework import serializers
from ..models.itemproducao import ItemProducao 
from ..models.lote import Lote


class ItemProducaoSerializer(serializers.ModelSerializer):
    maquina_nome = serializers.CharField(source='maquina.nome', read_only=True)
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)

    class Meta:
        model = ItemProducao
        fields = '__all__'