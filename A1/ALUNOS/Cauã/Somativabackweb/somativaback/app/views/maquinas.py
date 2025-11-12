from .__init__ import *
from ..models.maquinas import Maquina
from ..serializers.maquinas import MaquinaSerializer
from ..permissions import IsManutencaoOrEngenhariaOrAdmin, IsManutencaoOrAdmin, get_user_cargo 
from django.utils import timezone
from datetime import timedelta

class MaquinaViewSet(viewsets.ModelViewSet):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer
    permission_classes = [IsManutencaoOrEngenhariaOrAdmin]
    
    @action(detail=False, methods=['get'], permission_classes=[IsManutencaoOrAdmin])
    def manutencao_pendente(self, request):
        maquinas_pendentes = self.get_queryset().filter(
            ultima_data_manutencao__lt=timezone.now() - timedelta(days=90)
        )
        serializer = self.get_serializer(maquinas_pendentes, many=True)
        return Response(serializer.data)