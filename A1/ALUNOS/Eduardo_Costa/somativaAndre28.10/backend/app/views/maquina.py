from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from ..models import Maquina
from ..serializers import MaquinaSerializer
from ..permissions import Manutencao, Engenharia, Admin, Authenticated

class MaquinaView(ModelViewSet):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [Authenticated]
        else:
            permission_classes = [Manutencao | Engenharia | Admin]
        
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'], permission_classes=[Manutencao | Admin])
    def precisa_manutencao(self, request):
        tres_meses_atras = timezone.now().date() - timedelta(days=90)
        maquinas = Maquina.objects.filter(ultima_manutencao__lte=tres_meses_atras)
        
        serializer = self.get_serializer(maquinas, many=True)
        return Response({
            'total_maquinas': maquinas.count(),
            'maquinas': serializer.data
        })