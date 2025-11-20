from rest_framework import serializers
from ..models.lote import Lote
from .customuser import FuncionarioNomeSerializer 
from .itemproducao import ItemProducaoSerializer 

class LoteDetailSerializer(serializers.ModelSerializer):
    responsavel_inspecao = FuncionarioNomeSerializer(read_only=True)
    itens_produzidos = ItemProducaoSerializer(many=True, read_only=True)
    status_inspecao_display = serializers.CharField(source='get_status_inspecao_display', read_only=True)

    class Meta:
        model = Lote
        fields = '__all__'

class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = '__all__'