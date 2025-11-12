from rest_framework import serializers
from ..models import *

class MaquinaSerializer(serializers.ModelSerializer):
    from .funcionario import FuncionarioSerializer

    funcionario_fk = FuncionarioSerializer(read_only=True, many=False)
    
    class Meta:
        model = Maquina
        fields = '__all__'
        many= True