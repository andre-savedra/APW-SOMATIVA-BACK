from rest_framework import serializers
from .models import Hospede, Acomodacao, Reserva, Manutencao
from accounts.models import User

class HospedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospede
        fields = '__all__'

class AcomodacaoSerializer(serializers.ModelSerializer):
    funcionario_responsavel = serializers.StringRelatedField()
    class Meta:
        model = Acomodacao
        fields = '__all__'

class ReservaListSerializer(serializers.ModelSerializer):
    hospede_nome = serializers.CharField(source='hospede.nome_completo', read_only=True)
    acomodacao_numero = serializers.CharField(source='acomodacao.numero', read_only=True)
    class Meta:
        model = Reserva
        fields = ['id','codigo','check_in','check_out','valor_total','status','hospede','hospede_nome','acomodacao','acomodacao_numero']

class ReservaDetailSerializer(serializers.ModelSerializer):
    hospede = HospedeSerializer()
    acomodacao = AcomodacaoSerializer()
    class Meta:
        model = Reserva
        fields = '__all__'

class ReservaCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'

class ManutencaoSerializer(serializers.ModelSerializer):
    realizado_por = serializers.StringRelatedField()
    class Meta:
        model = Manutencao
        fields = '__all__'
