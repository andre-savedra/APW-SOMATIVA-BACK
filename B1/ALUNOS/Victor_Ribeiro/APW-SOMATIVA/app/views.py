from rest_framework import viewsets, generics
from .models import Veiculo, Funcionario, Viagem, Manutencao
from .serializers import VeiculoSerializer, FuncionarioSerializer, ViagemSerializer, ManutencaoSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ViagemFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import UserCreateSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = []  


class FuncionarioCreateView(generics.CreateAPIView):
    serializer_class = FuncionarioSerializer

class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        user = self.request.user
       
        if hasattr(user, 'funcionario'):
            cargo = user.funcionario.cargo
            if cargo in ['SUPERVISOR', 'ADMIN']:
                return [IsAuthenticated()]
        return [IsAdminUser()]


class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        user = self.request.user
        if user.funcionario.cargo == 'ENGENHEIRO' and self.action == 'create':
            return [IsAuthenticated()]  
        elif user.funcionario.cargo in ['SUPERVISOR', 'ADMIN']:
            return [IsAuthenticated()]  
        return [IsAdminUser()]


class ViagemViewSet(viewsets.ModelViewSet):
    queryset = Viagem.objects.all()
    serializer_class = ViagemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ViagemFilter

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'funcionario'):
            cargo = user.funcionario.cargo
            if cargo == 'MOTORISTA':
               
                return Viagem.objects.filter(
                    motorista=user.funcionario
                ) | Viagem.objects.filter(data_inicio__gt=timezone.now())
            elif cargo in ['ENGENHEIRO', 'SUPERVISOR', 'ADMIN']:
                return Viagem.objects.all() 
        return Viagem.objects.none()  


class ManutencaoViewSet(viewsets.ModelViewSet):
    queryset = Manutencao.objects.all()
    serializer_class = ManutencaoSerializer
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        user = self.request.user
        if hasattr(user, 'funcionario') and user.funcionario.cargo != 'SUPERVISOR':
            return Response({'error': 'Você não tem permissão para acessar este recurso.'}, status=403)

   
        data_inicio = request.query_params.get('data_inicio', None)
        data_termino = request.query_params.get('data_termino', None)
        categoria = request.query_params.get('categoria', None)

        viagens = Viagem.objects.all()
        manutencao = Manutencao.objects.all()

        
        if data_inicio:
            viagens = viagens.filter(data_inicio__gte=data_inicio)
            manutencao = manutencao.filter(data__gte=data_inicio)
        if data_termino:
            viagens = viagens.filter(data_termino__lte=data_termino)
            manutencao = manutencao.filter(data__lte=data_termino)
        if categoria:
            viagens = viagens.filter(veiculo__categoria=categoria)
            manutencao = manutencao.filter(veiculo__categoria=categoria)

        
        total_viagens = viagens.count()
        total_manutencao = manutencao.count()

       
        return Response({
            'total_viagens': total_viagens,
            'total_manutencao': total_manutencao,
        })