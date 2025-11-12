from rest_framework.viewsets import ModelViewSet
from ..models import *
from ..serializers import *
from ..permissions import *
from django.db.models import Q

class LoteView(ModelViewSet):
    serializer_class = LoteSerializer
   
    
    def get_permissions(self):
        """Define permissões diferentes para cada ação"""
        if self.action in ['list', 'retrieve']:  # GET
            # Engenharia pode ver, mas não editar
            permission_classes = [Authenticated]
        else:  # POST, PUT, PATCH, DELETE
            # Apenas Produção e Admin podem criar/editar
            permission_classes = [Producao | Admin]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        
        # Admin vê tudo
        if user.cargo == 'Admin':
            return Lote.objects.all()
        
        # Inspeção vê apenas não inspecionados OU inspecionados por ele
        if user.cargo == 'Inspecao':
            return Lote.objects.filter(
                Q(status_inspecao__isnull=True) | Q(responsavel_inspecao=user)
            )
        
        # Engenharia vê tudo (mas não pode editar - bloqueado em get_permissions)
        if user.cargo == 'Engenharia':
            return Lote.objects.all()
        
        # Produção vê tudo
        if user.cargo == 'Producao':
            return Lote.objects.all()
        
        return Lote.objects.none()