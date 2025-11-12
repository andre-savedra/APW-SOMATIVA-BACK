# app/views.py
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime, timedelta

from .models import Funcionario, Veiculo, Viagem, Manutencao
from .serializers import FuncionarioSerializer, VeiculoSerializer, ViagemSerializer, ManutencaoSerializer
from .permissions import CargoPermission  # import correto
from rest_framework import serializers

# Serializador customizado para incluir nome do motorista e modelo do veículo
class ViagemListSerializer(serializers.ModelSerializer):
    motorista_nome = serializers.CharField(source='motorista.nome', read_only=True)
    veiculo_modelo = serializers.CharField(source='veiculo.modelo', read_only=True)

    class Meta:
        model = Viagem
        fields = ['id', 'codigo', 'data_inicio', 'data_fim', 'destino', 'quilometragem',
                  'motorista', 'motorista_nome', 'veiculo', 'veiculo_modelo']


class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
    permission_classes = [permissions.IsAdminUser]


class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    permission_classes = [CargoPermission]


class ViagemViewSet(viewsets.ModelViewSet):
    queryset = Viagem.objects.all()
    serializer_class = ViagemListSerializer
    permission_classes = [CargoPermission]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['veiculo', 'veiculo__categoria', 'data_inicio', 'data_fim', 'quilometragem']

    def get_queryset(self):
        qs = super().get_queryset()
        cargo = getattr(self, 'cargo_user', None)

        if cargo == 'MOTORISTA':
            # Motoristas veem apenas suas viagens ou viagens ainda não iniciadas
            return qs.filter(motorista__usuario=self.request.user) | qs.filter(data_inicio__gt=datetime.now())
        elif cargo == 'ENGENHEIRO':
            # Engenheiros veem tudo, só leitura
            return qs
        elif cargo == 'SUPERVISOR_FROTA':
            return qs
        elif cargo == 'ADMIN':
            return qs
        return Viagem.objects.none()

    def get_serializer_class(self):
        # Pode-se usar serializer diferente para list e retrieve se quiser
        return ViagemListSerializer


class ManutencaoViewSet(viewsets.ModelViewSet):
    queryset = Manutencao.objects.all()
    serializer_class = ManutencaoSerializer
    permission_classes = [CargoPermission]

    @action(detail=False, methods=['get'])
    def veiculos_mais_de_60_dias(self, request):
        limite = datetime.now().date() - timedelta(days=60)
        veiculos = Veiculo.objects.filter(data_ultima_manutencao__lt=limite)
        serializer = VeiculoSerializer(veiculos, many=True)
        return Response(serializer.data)
