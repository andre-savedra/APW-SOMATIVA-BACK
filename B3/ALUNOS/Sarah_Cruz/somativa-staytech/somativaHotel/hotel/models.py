from django.db import models
from django.conf import settings

# Create your models here.

class Hospede(models.Model):
    nome_completo = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=30, blank=True)
    data_cadastro = models.DateField(auto_now_add=True)
    nacionalidade = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_completo

class Acomodacao(models.Model):
    TIPO_CHOICES = [
        ('standard','Standard'),
        ('suite','Suíte'),
        ('master','Master'),
    ]
    STATUS_CHOICES = [
        ('disponivel','Disponível'),
        ('ocupada','Ocupada'),
        ('manutencao','Em manutenção'),
    ]
    numero = models.CharField(max_length=20, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    capacidade_maxima = models.PositiveIntegerField()
    valor_diaria = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel')
    data_ultima_limpeza = models.DateField(null=True, blank=True)
    funcionario_responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                                on_delete=models.SET_NULL, related_name='limpezas')

    def __str__(self):
        return f"Apt {self.numero} - {self.tipo}"

class Reserva(models.Model):
    STATUS_RES = [
        ('ativa','Ativa'),
        ('finalizada','Finalizada'),
        ('cancelada','Cancelada'),
    ]
    codigo = models.CharField(max_length=50, unique=True)
    check_in = models.DateField()
    check_out = models.DateField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_RES, default='ativa')
    hospede = models.ForeignKey(Hospede, on_delete=models.CASCADE, related_name='reservas')
    acomodacao = models.ForeignKey(Acomodacao, on_delete=models.PROTECT, related_name='reservas')
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.codigo} - {self.hospede.nome_completo}"

class Manutencao(models.Model):
    acomodacao = models.ForeignKey(Acomodacao, on_delete=models.CASCADE, related_name='manutencoes')
    data = models.DateField(auto_now_add=True)
    descricao = models.TextField()
    realizado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Manut. {self.acomodacao.numero} - {self.data}"
