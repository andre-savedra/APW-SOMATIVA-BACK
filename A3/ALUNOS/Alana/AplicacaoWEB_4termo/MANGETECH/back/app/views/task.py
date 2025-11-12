from rest_framework.viewsets import ModelViewSet
from ..models import *
from ..serializers import *
from ..filters import TaskFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from ..utils import is_Admin

class TaskView(ReadWriteSerializer, ModelViewSet):
    queryset = Task.objects.all() #Inicialmente tem acesso a toda(all) tabela(class)
    read_serializer_class = TaskReadSerializer
    write_serializer_class = TaskWriteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter #puxa a classe de filtro 
    # permission_classes = [IsAuthenticated] #Só os usuários autenticados podem chamar esse endpoint 

    # def get_queryset(self):
    #    user = self.request.user
    #    if user.is_authenticated: #se o usuario(user) estiver autenticado
    #        return Task.objects.all() if is_Admin(user.id) else \
    #               Task.objects.filter(creator_FK=user.id) #retorna tudo se o user for Admin, se não filtar emostrar apenas o que tiver o mesmo id do use
    #    return Task.objects.none() #se não tiver autenticado não vê nada