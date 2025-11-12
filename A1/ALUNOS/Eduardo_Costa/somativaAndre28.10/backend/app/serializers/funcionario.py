from rest_framework import serializers
from ..models import *

class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = ['id','nome','email','cpf','numero_registro']
        many= True