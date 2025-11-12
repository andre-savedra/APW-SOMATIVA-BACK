from rest_framework import serializers
from .models import Hospede, Acomodacao, Empregado, Reservas, Limpeza, Manutencoes


class HospedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospede
        fields = '__all__'


class EmpregadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empregado
        fields = '__all__'


class LimpezaSerializer(serializers.ModelSerializer):
    empreado = EmpregadoSerializer(read_only=True)
    empreado_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Empregado.objects.all(), source='empreado', required=False, allow_null=True)

    class Meta:
        model = Limpeza
        fields = ['id', 'acomodacao', 'empreado', 'empreado_id', 'ultima_vez_limpo', 'nota']


class ManutencoesSerializer(serializers.ModelSerializer):
    empregado = EmpregadoSerializer(read_only=True)
    empregado_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Empregado.objects.all(),
        source='empregado',
        required=False,
        allow_null=True
    )

    class Meta:
        model = Manutencoes
        fields = ['id', 'acomodacao', 'empregado', 'empregado_id', 'descricao']


class AcomodacaoSerializer(serializers.ModelSerializer):
    # ultima_limpeza = serializers.SerializerMethodField()


    class Meta:
        model = Acomodacao
        fields = ['id', 'numero', 'tipo', 'capacidade_maxima', 'avaliacao_diaria', 'status', 'data_ultimaLimpeza']


class ReservasSerializer(serializers.ModelSerializer):
    hospede_nome = serializers.CharField(source='hospede.nome_inteiro', read_only=True)
    acomodacao_numero = serializers.CharField(source='acomodacao.numero', read_only=True)


    class Meta:
        model = Reservas
        fields = ['id', 'codigo', 'hospede','hospede_nome' ,'acomodacao', 'acomodacao_numero', 'check_in', 'check_out', 'valor_total', 'status', 'criado_em']


class ReservasSerializer(serializers.ModelSerializer):
    hospede_nome = serializers.CharField(source='hospede.nome', read_only=True)
    acomodacao_numero = serializers.CharField(source='acomodacao.numero', read_only=True)

    class Meta:
        model = Reservas
        fields = ['id', 'codigo', 'check_in', 'check_out', 'valor_total', 'status',
                  'hospede_nome', 'acomodacao_numero']

from rest_framework import serializers
from .models import Empregado

class EmpregadoRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Empregado
        fields = ['id', 'registro', 'nome', 'cargo', 'data_contratacao', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Empregado.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user