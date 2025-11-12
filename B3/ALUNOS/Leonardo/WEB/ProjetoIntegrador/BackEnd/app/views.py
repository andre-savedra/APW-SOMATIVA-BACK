from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .utils import isAdmin
from .filters import tarefas_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

#Essas duas linhas queryset e serializers vai fazer o GET, PUT, POST e DELETE

class CustomUserView(ModelViewSet):    
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class AmbienteView(ModelViewSet):    
    queryset = Ambiente.objects.all()
    serializer_class = AmbienteSerializer

class AtivoView(ModelViewSet):    
    queryset = Ativo.objects.all()
    serializer_class = AtivoSerializer

class TarefasView(ModelViewSet):    
    queryset = Tarefas.objects.all()
    serializer_class = TarefasSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = tarefas_filters
    ordering_fields = '__all__'

    def get_queryset(self):
        user = self.request.user
        #select * from Task WHERE creator_FK = user.id
        if user.is_authenticated:
            return Tarefas.objects.all() if isAdmin(user.id) \
                else Tarefas.objects.filter(responsibles=user.id)
        return Tarefas.objects.none()

class HistoricoStatusView(ModelViewSet):    
    queryset = HistoricoStatus.objects.all()
    serializer_class = HistoricoStatusSerializer

class TarefaStatusImageView(ModelViewSet):    
    queryset = TarefaStatusImage.objects.all()
    serializer_class = TarefaStatusImageSerializer

class NotificationView(ModelViewSet):    
    queryset = Notification.objects.all()
    serializer_class = NoificationSerializer

class CategoryView(ModelViewSet):
    queryset = Category.objects.all() #qual a tabela e a query
    serializer_class = CategorySerializer #qual o serializer