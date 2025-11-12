from rest_framework import viewsets, status
from rest_framework.permissions import  BasePermission, IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from .models import *
from .serializers import *

class IsGovernanca(BasePermission):
    """Permite acesso apenas a usuários com cargo GOVERNANCA."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.cargo == 'GOVERNANCA'

class HospedeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Hospede.objects.all()
    serializer_class = HospedeSerializer


class AcomodacaoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Acomodacao.objects.all()
    serializer_class = AcomodacaoSerializer

    def update(self, request, *args, **kwargs):
        user = request.user
        if user.cargo == 'GOVERNANCA':
            campos_permitidos = ['data_ultima_limpeza', 'funcionario_responsavel']
            for campo in request.data:
                if campo not in campos_permitidos:
                    return Response({'erro': 'Governança só pode atualizar limpeza e responsável.'}, status=403)
        elif user.cargo == 'MANUTENCAO':
            if 'status' not in request.data:
                return Response({'erro': 'Manutenção só pode alterar status.'}, status=403)
        return super().update(request, *args, **kwargs)


class ReservaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

    def get_queryset(self):
        qs = Reserva.objects.all()
        params = self.request.query_params
        if params.get('status'):
            qs = qs.filter(status=params['status'])
        if params.get('tipo'):
            qs = qs.filter(acomodacao__tipo=params['tipo'])
        if params.get('nacionalidade'):
            qs = qs.filter(hospede__nacionalidade__icontains=params['nacionalidade'])
        if params.get('check_in') and params.get('check_out'):
            qs = qs.filter(check_in__gte=params['check_in'], check_out__lte=params['check_out'])
        return qs

    def destroy(self, request, *args, **kwargs):
        if request.user.cargo == 'RECEPCAO':
            return Response({'erro': 'Recepção não pode excluir reservas.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class GovernancaPendentesViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsGovernanca]
    def list(self, request):
        limite = timezone.now().date() - timezone.timedelta(days=7)
        pendentes = Acomodacao.objects.filter(
            Q(data_ultima_limpeza__lt=limite) | Q(data_ultima_limpeza__isnull=True)
        )
        serializer = AcomodacaoSerializer(pendentes, many=True)
        return Response(serializer.data)


class ManutencaoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Manutencao.objects.all()
    serializer_class = ManutencaoSerializer
