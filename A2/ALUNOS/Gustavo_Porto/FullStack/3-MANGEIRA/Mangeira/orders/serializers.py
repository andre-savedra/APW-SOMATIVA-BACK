from rest_framework import serializers
from .models import Pedido, ItemPedido, CartaoCredito, Devolucao
from store.serializers import ProdutoSerializer

# Item do Pedido
class ItemPedidoSerializer(serializers.ModelSerializer):
    produto = ProdutoSerializer(read_only=True)

    class Meta:
        model = ItemPedido
        fields = ['id', 'produto', 'quantidade', 'preco_unitario']

# Pedido
class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'usuario', 'status', 'metodo_pagamento', 'valor_total', 'valor_desconto', 'codigo_rastreamento', 'itens', 'criado_em']

# Cartão de Crédito
class CartaoCreditoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartaoCredito
        fields = ['numero', 'nome_titular', 'validade', 'codigo']

# Devolução
class DevolucaoSerializer(serializers.ModelSerializer):
    pedido = PedidoSerializer(read_only=True)
    item = ItemPedidoSerializer(read_only=True)

    class Meta:
        model = Devolucao
        fields = ['id', 'pedido', 'item', 'motivo', 'data_solicitacao']
