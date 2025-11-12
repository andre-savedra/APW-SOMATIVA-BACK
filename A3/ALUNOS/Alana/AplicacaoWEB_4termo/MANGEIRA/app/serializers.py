from rest_framework import serializers
from .models import *

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        many = True
        
class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
       model = Produto
       fields = '__all__'
       many = True

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
       model = Pedido
       fields = '__all__'
       many = True


