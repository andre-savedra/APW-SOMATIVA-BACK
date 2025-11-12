from rest_framework import serializers
from .models import Hospede, Acomodacao, Reserva, Funcionario, Manutencao

class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = ['id', 'email', 'nome', 'cargo', 'matricula', 'data_contratacao']


class HospedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospede
        fields = '__all__'


class AcomodacaoSerializer(serializers.ModelSerializer):
    funcionario_responsavel = FuncionarioSerializer(read_only=True)

    class Meta:
        model = Acomodacao
        fields = '__all__'


class ReservaSerializer(serializers.ModelSerializer):
    valor_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    hospede_nome = serializers.CharField(source='hospede.nome_completo', read_only=True)
    acomodacao_numero = serializers.IntegerField(source='acomodacao.numero', read_only=True)

    class Meta:
        model = Reserva
        fields = '__all__'


class ManutencaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manutencao
        fields = '__all__'
