from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import (
    Funcionario, Veiculo, Viagem, Manutencao, CategoriaVeiculo, Funcionario
)
from .serializers import (
    FuncionarioSerializer, VeiculoSerializer, ViagemSerializer, 
    ManutencaoSerializer, CategoriaVeiculoSerializer
)
from .filters import ViagemFilter

from .permissions import (
    ViagemPermission, 
    CategoriaVeiculoPermission,
    ManutencaoPermission,
    AdminSupervisorFullAccessReadOnlyOthers,
    DashboardAccessPermission,
    IsMecanicoOrAdminSupervisor,
)

class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
    
    permission_classes = [IsAuthenticated, AdminSupervisorFullAccessReadOnlyOthers]

class CategoriaVeiculoViewSet(viewsets.ModelViewSet):
    queryset = CategoriaVeiculo.objects.all()
    serializer_class = CategoriaVeiculoSerializer
   
    permission_classes = [IsAuthenticated, CategoriaVeiculoPermission]


class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    
    permission_classes = [IsAuthenticated, AdminSupervisorFullAccessReadOnlyOthers]


class ViagemViewSet(viewsets.ModelViewSet):
    serializer_class = ViagemSerializer
    permission_classes = [IsAuthenticated, ViagemPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ViagemFilter
    
    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Viagem.objects.all()
        
        try:
            cargo = user.funcionario.cargo
            funcionario_atual = user.funcionario
        except Funcionario.DoesNotExist:
            return Viagem.objects.none()

        if cargo == Funcionario.Cargos.MOTORISTA:
            # ... (lógica do motorista)
            agora = timezone.now()
            filtro_motorista = Q(motorista=funcionario_atual)
            filtro_nao_iniciada = Q(data_hora_inicio__gt=agora)
            return Viagem.objects.filter(filtro_motorista | filtro_nao_iniciada)
        
      
      
        elif cargo in [
            Funcionario.Cargos.ADMIN, 
            Funcionario.Cargos.SUPERVISOR_FROTA,
            Funcionario.Cargos.ENGENHEIRO,
            Funcionario.Cargos.MECANICO
        ]:
        
            return Viagem.objects.all()
        
        else:
            return Viagem.objects.none()

   
class ManutencaoViewSet(viewsets.ModelViewSet):
    queryset = Manutencao.objects.all()
    serializer_class = ManutencaoSerializer
    
    permission_classes = [IsAuthenticated, ManutencaoPermission]    


class DashboardView(APIView):
    """
    Endpoint de API para o dashboard de Supervisor de Frota.
    Retorna estatísticas agregadas com base em filtros de
    período (data_inicio, data_fim) e categoria de veículo (categoria).
    """
  
    permission_classes = [IsAuthenticated, DashboardAccessPermission]

    def get(self, request, *args, **kwargs):
       
        data_inicio = request.query_params.get('data_inicio', None)
        data_fim = request.query_params.get('data_fim', None)
        categoria_id = request.query_params.get('categoria', None)

        
        viagens_qs = Viagem.objects.all()
        manutencoes_qs = Manutencao.objects.all()

       
        filtros_aplicados = {}

        if data_inicio:
            viagens_qs = viagens_qs.filter(data_hora_inicio__gte=data_inicio)
            manutencoes_qs = manutencoes_qs.filter(data__gte=data_inicio)
            filtros_aplicados['data_inicio'] = data_inicio

        if data_fim:
            viagens_qs = viagens_qs.filter(data_hora_inicio__lte=data_fim)
            manutencoes_qs = manutencoes_qs.filter(data__lte=data_fim)
            filtros_aplicados['data_fim'] = data_fim
        
        if categoria_id:
            
            viagens_qs = viagens_qs.filter(veiculo__categoria_id=categoria_id)
            manutencoes_qs = manutencoes_qs.filter(veiculo__categoria_id=categoria_id)
            
            try:
                categoria_nome = CategoriaVeiculo.objects.get(id=categoria_id).nome
                filtros_aplicados['categoria'] = f"ID {categoria_id} ({categoria_nome})"
            except CategoriaVeiculo.DoesNotExist:
                filtros_aplicados['categoria'] = f"ID {categoria_id} (inválido)"
        
        total_viagens = viagens_qs.count()
        
        total_manutencoes_preventivas = manutencoes_qs.filter(
            tipo=Manutencao.TiposManutencao.PREVENTIVA
        ).count()
        
        total_manutencoes_corretivas = manutencoes_qs.filter(
            tipo=Manutencao.TiposManutencao.CORRETIVA
        ).count()

        data = {
            'filtros_aplicados': filtros_aplicados,
            'total_viagens': total_viagens,
            'total_manutencoes_preventivas': total_manutencoes_preventivas,
            'total_manutencoes_corretivas': total_manutencoes_corretivas
        }
        
        return Response(data)
    

class VeiculosManutencaoAtrasadaView(generics.ListAPIView):
    """
    Endpoint exclusivo para Mecânicos (e gestão)
    que lista veículos com manutenção atrasada
    (última manutenção > 60 dias ou nunca realizada).
    """
    serializer_class = VeiculoSerializer
    
    permission_classes = [IsAuthenticated, IsMecanicoOrAdminSupervisor]

    def get_queryset(self):
        hoje = timezone.now().date()
        
        limite = hoje - timedelta(days=60)
        

        filtro_vencida = Q(data_ultima_manutencao__lt=limite)
        

        filtro_nunca_feita = Q(data_ultima_manutencao__isnull=True)
        
        return Veiculo.objects.filter(filtro_vencida | filtro_nunca_feita)