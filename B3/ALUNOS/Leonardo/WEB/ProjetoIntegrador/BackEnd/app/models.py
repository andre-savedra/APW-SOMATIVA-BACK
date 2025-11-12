from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .user_manager import CustomUserManager
from django.utils import timezone

# Create your models here.

STATUS = [
    ('OPEN', 'Aberto'),
    ('WAITING', 'Aguardando responsáveis'),
    ('IN PROCESS', 'Em andamento'),
    ('PERFORMED', 'Realizado'),
    ('COMPLETED', 'Concluído'),
    ('CANCELED', 'Cancelado'),
]

URGENCY_LEVELS = [
    ('LOW', 'Baixa'),
    ('MEDIUM', 'Média'),
    ('HIGH', 'Alta'),
]


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    cpf = models.CharField(max_length=12, unique=True)
    registro = models.CharField(max_length=12, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    photo = models.FileField(upload_to='user_images', null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    #pode acessar tela admin do django ou não
    is_staff = models.BooleanField(default=False)

    #se o usuário está ativo ou não
    is_active = models.BooleanField(default=True) #Confirmação de email do usuario

    #login por email
    USERNAME_FIELD = 'name'

    #o que é obrigatório além do padrão (username, email, password)
    REQUIRED_FIELDS = ['email','cpf', 'registro']

    objects = CustomUserManager()

class Ambiente(models.Model):
    name = models.CharField(max_length=255)
    responsible = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,  
        null=True,
        blank=True,
        related_name='ambientes_responsaveis'  
    )

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
    
class Ativo(models.Model):
    name = models.CharField(max_length=200, default='Sem nome')
    number = models.CharField(max_length=12, unique=True)
    description = models.CharField(max_length=1000)
    ambientes = models.ForeignKey(Ambiente, related_name='ativos',on_delete=models.SET_NULL,null=True)
    creation_date = models.DateTimeField(auto_now_add=True, null=True)
    category_FK = models.ForeignKey(Category,related_name='Equipment_category_FK',on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return f'{self.number}-{self.name}'

class Tarefas(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    status = models.CharField(max_length=100, choices=STATUS)
    start_date_status = models.DateTimeField(auto_now_add=True)
    suggested_date = models.DateTimeField(null=True, blank=True)
    resolution_date = models.DateTimeField(null=True, blank=True)
    responsibles = models.ManyToManyField(CustomUser)
    ativos = models.ForeignKey(Ativo, on_delete=models.CASCADE)
    urgency = models.CharField(max_length=50, choices=URGENCY_LEVELS,
                                     default='LOW')

    def __str__(self):
        return self.name
    
class HistoricoStatus(models.Model):
    tarefa = models.ForeignKey(Tarefas,
                                related_name='TaskStatus_task_FK',
                                on_delete=models.CASCADE)
    status_anterior = models.CharField(max_length=100, choices=STATUS)
    novo_status = models.CharField(max_length=100, choices=STATUS)
    descricao = models.CharField(max_length=300, null=True, blank=True)
    data_alteracao = models.DateTimeField(auto_now_add=True)
    alterado_por = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='historicos_alterados')

    def __str__(self):
        return f'{self.tarefa}-{self.novo_status}'
    
class TarefaStatusImage(models.Model):
    image = models.FileField(upload_to='task_images')
    tarefa = models.ForeignKey(Tarefas,
                                related_name='TaskStatusImage_task_FK',
                                on_delete=models.CASCADE)
    

    def __str__(self):
        return f'{self.tarefa.id}-{self.id}'
    
class Notification(models.Model):
    text = models.CharField(max_length=500)
    task_FK = models.ForeignKey(Tarefas,
                                related_name='Notification_task_FK',
                                on_delete=models.CASCADE)
    user_FK = models.ForeignKey(CustomUser,
                                related_name='Notification_user_FK',
                                on_delete=models.SET_NULL,
                                null=True)
    creation_date = models.DateTimeField(auto_now_add=True)    
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.task_FK.id}-{self.text}'




