from rest_framework import serializers
from ..models.customuser import Funcionario

class FuncionarioNomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = ['id', 'nome', 'cargo', 'numero_registro']