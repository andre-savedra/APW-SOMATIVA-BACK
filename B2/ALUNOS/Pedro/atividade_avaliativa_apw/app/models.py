from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Definindo os cargos possíveis
class Cargos(models.TextChoices): 
    PRODUCAO = 'PRODUCAO'
    CHEFE_PRODUCAO = 'CHEFE_PRODUCAO'
    INSPECAO = 'INSPECAO'
    MANUTENCAO = 'MANUTENCAO'
    ADMIN = 'ADMIN'

# Definindo o status possível
class Status(models.TextChoices):
    APROVADO = 'APROVADO'
    REPROVADO = 'REPROVADO'

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=25)
    descricao = models.CharField(max_length=1000)
    categoria = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    noregistro = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    cpf = models.CharField(max_length=100)
    data_contrato = models.DateTimeField(auto_now_add=True)
    cargo = models.CharField(max_length=50, choices=Cargos.choices)

    def __str__(self):
        return self.nome

class Manutencao(models.Model):
    data_hora = models.DateTimeField(auto_now_add=True)
    descricao = models.CharField(max_length=400)
    encarregado = models.ForeignKey(Funcionario, on_delete=models.CASCADE)

    def __str__(self):
        return self.descricao

class Maquina(models.Model):
    codigo = models.IntegerField()
    foto = models.ImageField(upload_to="maquinas/fotos/")
    descricao = models.CharField(max_length=3000)
    historico = models.ManyToManyField(Manutencao, blank=True)

    def __str__(self):
        return str(self.codigo)

class Lote(models.Model):
    codigo = models.CharField(max_length=25)
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_final = models.DateTimeField(null=True, blank=True)
    data_inspecao = models.DateField(null=True, blank=True)
    encarregado_inspecao = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True)
    status_inspecao = models.CharField(max_length=50, choices=Status.choices)
    produtos = models.ManyToManyField(Produto, blank=True)
    maquina = models.ForeignKey(Maquina, on_delete=models.SET_NULL, null=True, blank=True)
    qrcode = models.ImageField(upload_to="Lote/qrcode/")

    def __str__(self):
        return self.codigo

class Producao(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    lote = models.ManyToManyField(Lote, blank=True)

    def __str__(self):
        return self.nome
