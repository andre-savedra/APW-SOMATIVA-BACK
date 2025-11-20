from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .models import Reservas, Hospede, Acomodacao, Empregado
from .serializers import ReservasSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .filters import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from .user_manager import IsGovernanceForCleaning, IsMaintenanceForAccommodation

class ReservasViewSet(ModelViewSet):
    queryset = Reservas.objects.all().order_by('-check_in')
    serializer_class = ReservasSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReservationFilter
    permission_classes = [IsAuthenticated]


class HospedeViewSet(ModelViewSet):
    queryset = Hospede.objects.all()
    serializer_class = HospedeSerializer

class AcomodacaoViewSet(ModelViewSet):
    queryset = Acomodacao.objects.all()
    serializer_class = AcomodacaoSerializer
    permission_classes = [IsAuthenticated]#, IsMaintenanceForAccommodation]


    @action(detail=False, methods=['get'], url_path='nao-limpas')
    def nao_limpas(self, request):
        limite = timezone.now().date() - timedelta(days=7)
        acomodacoes = self.queryset.filter(data_ultima_limpeza__lt=limite)
        serializer = self.get_serializer(acomodacoes, many=True)
        return Response(serializer.data)

class EmpregadoViewSet(ModelViewSet):
    queryset = Empregado.objects.all()
    serializer_class = EmpregadoSerializer
    permission_classes = [IsAuthenticated]

class LimpezaViewSet(ModelViewSet):
    queryset = Limpeza.objects.all()
    serializer_class = LimpezaSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated, IsGovernanceForCleaning]

class ManutencoesViewSet(ModelViewSet):
    queryset = Manutencoes.objects.all()
    serializer_class = ManutencoesSerializer
    permission_classes = [IsAuthenticated]


class CustomAuthToken(APIView):
    def post(self, request):
        registro = request.data.get('registro')
        password = request.data.get('password')

        user = authenticate(request, registro=registro, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'name': user.username            
            })
        return Response({'error': 'Usuário ou senha incorretos'}, status=status.HTTP_401_UNAUTHORIZED)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        try:
            empregado = Empregado.objects.get(registro=request.user.username)
        except Empregado.DoesNotExist:
            return Response({"detail": "Empregado não encontrado."}, status=404)

        empregado_data = {
            'id': empregado.id,
            'nome': empregado.nome,
            'registro': empregado.registro,
            'cargo': empregado.cargo,
            'data_contratacao': empregado.data_contratacao,
            'usuario': request.user.username
        }

        return Response(empregado_data)
    

from rest_framework.permissions import IsAdminUser

class EmpregadoCreateView(generics.CreateAPIView):
    queryset = Empregado.objects.all()
    serializer_class = EmpregadoRegisterSerializer
