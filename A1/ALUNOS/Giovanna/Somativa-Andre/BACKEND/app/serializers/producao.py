from rest_framework import serializers
from ..models import *

class ProducaoSerializer(serializers.ModelSerializer):
    funcionario = serializers.CharField(source='responsavel_inspecao.username', read_only=True)
    class Meta:
        model = Producao
        fields = [
            'id',
            'data_producao',
            'status',
            'maquina_FK',
            'produto_FK',
            'lote_FK',
            'funcionario',  
        ]


