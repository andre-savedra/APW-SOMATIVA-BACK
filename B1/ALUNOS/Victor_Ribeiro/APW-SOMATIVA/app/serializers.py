from rest_framework import serializers
from .models import Veiculo, Funcionario, Viagem, Manutencao
from django.contrib.auth.models import User
from app.models import Funcionario

class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = '__all__'

class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = '__all__'

class ViagemSerializer(serializers.ModelSerializer):
    motorista = serializers.StringRelatedField()
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    veiculo_modelo = serializers.CharField(source='veiculo.modelo', read_only=True)
    
    class Meta:
        model = Viagem
        fields = [
            'id', 'motorista', 'veiculo', 'veiculo_placa', 'veiculo_modelo',
            'codigo_id', 'data_inicio', 'hora_inicio', 'data_termino', 'hora_termino',
            'destino', 'km'
        ]

class ManutencaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manutencao
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class FuncionarioSerializer(serializers.ModelSerializer):
    nome = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Funcionario
        fields = ['id', 'nome', 'matricula', 'email', 'cpf', 'data_contratacao', 'cargo']

    def create(self, validated_data):
        nome_data = validated_data.pop('nome', None)
        
        
        if not nome_data:
            user = User.objects.create_user(username=validated_data['email'], password='password_default')  # Senha padrão ou definida
            validated_data['nome'] = user

        return Funcionario.objects.create(**validated_data)