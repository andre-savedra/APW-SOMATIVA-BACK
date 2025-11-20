from rest_framework.viewsets import ModelViewSet
from ..models import *
from ..serializers import *
from ..utils import is_Admin, is_Manutencao, is_Engenharia
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from rest_framework.views import APIView

class MaquinaView(ModelViewSet):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        if not (is_Manutencao(user) or is_Engenharia(user) or is_Admin(user)):
            return Response(
                {"detail": "Apenas manutenção, engenharia ou admin podem criar máquinas."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.user
        if not (is_Manutencao(user) or is_Engenharia(user) or is_Admin(user)):
            return Response(
                {"detail": "Apenas manutenção, engenharia ou admin podem editar máquinas."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if not is_Admin(user):
            return Response(
                {"detail": "Apenas admin pode deletar máquinas."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
    

class MaquinasPendentesManutencaoView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if not is_Manutencao(user):
            return Response(
                {"detail": "Apenas funcionários de manutenção podem acessar este endpoint."},
                status=status.HTTP_403_FORBIDDEN
            )
        hoje = datetime.now()
        tres_meses_atras = hoje - timedelta(days=90)

        maquinas_pendentes = Maquina.objects.filter(
            data_manutencao__lt=tres_meses_atras
        ) | Maquina.objects.filter(
            data_manutencao__isnull=True
        )
        serializer = MaquinaSerializer(maquinas_pendentes, many=True)
        return Response(serializer.data)
