from rest_framework import viewsets
from ..models.manutencao import Manutencao
from ..serializers.manutencao import ManutencaoSerializer
# CORREÇÃO CRUCIAL: Importa a permissão que estava faltando
from ..permissions import IsManutencaoOrEngenhariaOrAdmin, IsManutencaoOrAdmin


class ManutencaoViewSet(viewsets.ModelViewSet):
    queryset = Manutencao.objects.all()
    serializer_class = ManutencaoSerializer
    # Agora a classe está definida!
    permission_classes = [IsManutencaoOrEngenhariaOrAdmin]