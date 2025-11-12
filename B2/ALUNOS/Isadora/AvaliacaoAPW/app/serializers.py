from rest_framework import serializers 
from .models import *


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'
    
class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = '__all__'
        
class ItensLoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItensLote
        fields = '__all__'
        
class MaquinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maquina
        fields = '__all__'
    
class ManutencaoSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Manutencao
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'