from rest_framework import serializers
from .models import Hospede, Acomodacao, Empregado, Reservas, Limpeza, Manutencoes

from rest_framework import serializers
from .models import Empregado


class HospedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospede
        fields = '__all__'


class EmpregadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empregado
        fields = '__all__'


class LimpezaSerializer(serializers.ModelSerializer):
    empregado = serializers.CharField(source='empregado.nome', read_only=True)
    acomodacao_numero = serializers.CharField(source='acomodacao.numero', read_only=True)
    
    empregado_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Empregado.objects.all(),
        source='empregado',
        required=False,
        allow_null=True
    )

    class Meta:
        model = Limpeza
        fields = [
            'id',
            'acomodacao',
            'empregado',
            'acomodacao_numero',
            'empregado_id',
            'ultima_vez_limpo',
            'nota'
        ]

    def update(self, instance, validated_data):
      
        user = self.context['request'].user
        cargo = getattr(user, 'cargo', None)

        if cargo == 'Governanca':
            allowed_fields = {'ultima_vez_limpo', 'nota'}
            validated_data = {k: v for k, v in validated_data.items() if k in allowed_fields}

        return super().update(instance, validated_data)


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
    limpeza = LimpezaSerializer(read_only=True)
    ultima_limpeza = serializers.SerializerMethodField()


    class Meta:
        model = Acomodacao
        fields = ['id', 'numero', 'tipo', 'capacidade_maxima', 'avaliacao_diaria', 'status', 'limpeza','ultima_limpeza']

    def update(self, instance, validated_data):
        user = self.context['request'].user
        cargo = getattr(user, "cargo", None)

        if cargo == "Manutencao":
            
            validated_data = {k: v for k, v in validated_data.items() if k == "status"}

        return super().update(instance, validated_data)
    
    
    def get_ultima_limpeza(self, obj):
        limpeza = Limpeza.objects.filter(acomodacao=obj).order_by('-ultima_vez_limpo').first()
        if limpeza:
            return LimpezaSerializer(limpeza).data
        return None


class ReservasSerializer(serializers.ModelSerializer):
    hospede_nome = serializers.CharField(source='hospede.nome_inteiro', read_only=True)
    acomodacao_tipo = serializers.CharField(source='acomodacao.tipo', read_only=True)
    acomodacao_numero = serializers.CharField(source='acomodacao.numero', read_only=True)


    class Meta:
        model = Reservas
        fields = ['id', 'codigo', 'hospede','hospede_nome' ,'acomodacao', 'acomodacao_numero', 'acomodacao_tipo','check_in', 'check_out', 'valor_total', 'status', 'criado_em']

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