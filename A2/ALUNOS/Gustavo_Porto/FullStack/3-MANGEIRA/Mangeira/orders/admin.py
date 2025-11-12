from django.contrib import admin
from .models import Pedido, ItemPedido, CartaoCredito, Devolucao

admin.site.register(Pedido)
admin.site.register(ItemPedido)
admin.site.register(CartaoCredito)
admin.site.register(Devolucao)
