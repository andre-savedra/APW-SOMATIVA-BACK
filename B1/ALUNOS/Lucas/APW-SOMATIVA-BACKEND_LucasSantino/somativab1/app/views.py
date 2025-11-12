from datetime import timedelta
from django.utils import timezone
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Categoria, Funcionario, Veiculo, Viagem, Manutencao
from .serializers import (
    CategoriaSerializer, FuncionarioSerializer, VeiculoSerializer,
    ViagemSerializer, ManutencaoSerializer
)

def get_cargo_usuario(request):
    email = request.headers.get('X-Funcionario')
    if email:
        try:
            funcionario = Funcionario.objects.get(email=email)
            return funcionario.cargo
        except Funcionario.DoesNotExist:
            return None
    return None

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    def create(self, request, *args, **kwargs):
        cargo = get_cargo_usuario(request)
        if cargo not in ['ENGENHEIRO', 'ADMIN']:
            return Response({'detail': 'Apenas engenheiros ou admin podem criar categorias.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer

class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    def create(self, request, *args, **kwargs):
        cargo = get_cargo_usuario(request)
        if cargo not in ['SUPERVISOR_FROTA', 'ADMIN']:
            return Response({'detail': 'Apenas supervisores ou admin podem criar veículos.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        cargo = get_cargo_usuario(request)
        if cargo not in ['SUPERVISOR_FROTA', 'ADMIN']:
            return Response({'detail': 'Apenas supervisores ou admin podem editar veículos.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

class ViagemViewSet(viewsets.ModelViewSet):
    queryset = Viagem.objects.all()
    serializer_class = ViagemSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['destino', 'motorista__nome', 'veiculo__modelo']

    def get_queryset(self):
        queryset = Viagem.objects.all()
        cargo = get_cargo_usuario(self.request)
        data_inicio = self.request.query_params.get('data_inicio')
        data_fim = self.request.query_params.get('data_fim')
        veiculo = self.request.query_params.get('veiculo')
        categoria = self.request.query_params.get('categoria')
        quilometragem_minima = self.request.query_params.get('quilometragem_minima')

        if data_inicio and data_fim:
            queryset = queryset.filter(data_hora_inicio__range=[data_inicio, data_fim])
        if veiculo:
            queryset = queryset.filter(veiculo__num_placa=veiculo)
        if categoria:
            queryset = queryset.filter(veiculo__categoria__nome=categoria)
        if quilometragem_minima:
            queryset = queryset.filter(quilometragem__gte=quilometragem_minima)
        if cargo == 'MOTORISTA':
            funcionario = Funcionario.objects.filter(email=self.request.headers.get('X-Funcionario')).first()
            if funcionario:
                queryset = (
                    queryset.filter(motorista=funcionario)
                    | queryset.filter(data_hora_inicio__gt=timezone.now())
                ).distinct()
        return queryset

    def create(self, request, *args, **kwargs):
        cargo = get_cargo_usuario(request)
        if cargo == 'ENGENHEIRO':
            return Response({'detail': 'Engenheiros não podem criar viagens.'},
                            status=status.HTTP_403_FORBIDDEN)
        if cargo not in ['SUPERVISOR_FROTA', 'ADMIN']:
            return Response({'detail': 'Apenas supervisores ou admin podem criar viagens.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        cargo = get_cargo_usuario(request)
        if cargo == 'ENGENHEIRO':
            return Response({'detail': 'Engenheiros não podem editar viagens.'},
                            status=status.HTTP_403_FORBIDDEN)
        if cargo not in ['SUPERVISOR_FROTA', 'ADMIN']:
            return Response({'detail': 'Apenas supervisores ou admin podem editar viagens.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

class ManutencaoViewSet(viewsets.ModelViewSet):
    queryset = Manutencao.objects.all()
    serializer_class = ManutencaoSerializer
    def create(self, request, *args, **kwargs):
        cargo = get_cargo_usuario(request)
        if cargo not in ['MECANICO', 'ADMIN']:
            return Response({'detail': 'Apenas mecânicos ou admin podem registrar manutenções.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        cargo = get_cargo_usuario(request)
        if cargo not in ['MECANICO', 'ADMIN']:
            return Response({'detail': 'Apenas mecânicos ou admin podem editar manutenções.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='veiculos-atrasados')
    def veiculos_atrasados(self, request):
        cargo = get_cargo_usuario(request)
        if cargo not in ['MECANICO', 'ADMIN']:
            return Response({'detail': 'Apenas mecânicos ou admin podem acessar esta lista.'},
                            status=status.HTTP_403_FORBIDDEN)
        limite = timezone.now().date() - timedelta(days=60)
        veiculos_atrasados = (
            Veiculo.objects
            .filter(data_ultima_manutencao__lt=limite)
            .order_by('data_ultima_manutencao')
        )
        if not veiculos_atrasados.exists():
            return Response({'detail': 'Nenhum veículo está atrasado para manutenção.'},
                            status=status.HTTP_200_OK)
        serializer = VeiculoSerializer(veiculos_atrasados, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DashboardViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'], url_path='resumo')
    def resumo(self, request):
        cargo = get_cargo_usuario(request)
        if cargo not in ['SUPERVISOR_FROTA', 'ADMIN']:
            return Response({'detail': 'Acesso restrito ao supervisor de frota ou admin.'},
                            status=status.HTTP_403_FORBIDDEN)
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        categoria = request.query_params.get('categoria')
        viagens = Viagem.objects.all()
        manutencoes = Manutencao.objects.all()
        if data_inicio and data_fim:
            viagens = viagens.filter(data_hora_inicio__range=[data_inicio, data_fim])
            manutencoes = manutencoes.filter(data__range=[data_inicio, data_fim])
        if categoria:
            viagens = viagens.filter(veiculo__categoria__nome=categoria)
            manutencoes = manutencoes.filter(veiculo__categoria__nome=categoria)
        data = {
            'total_viagens': viagens.count(),
            'manutencoes_preventivas': manutencoes.filter(tipo='PREVENTIVA').count(),
            'manutencoes_corretivas': manutencoes.filter(tipo='CORRETIVA').count(),
        }
        return Response(data)
