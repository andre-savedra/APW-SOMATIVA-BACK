from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Cargo(models.TextChoices):
    PRODUCAO = 'PRODUCAO', 'Produção'
    LIDER_PRODUCAO = 'LIDER_PRODUCAO', 'Líder de Produção'
    INSPECAO = 'INSPECAO', 'Inspeção'
    MANUTENCAO = 'MANUTENCAO', 'Manutenção'
    ADMIN = 'ADMIN', 'Administrador'


class Funcionario(AbstractUser):
    numero_registro = models.CharField(max_length=20, unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    data_contratacao = models.DateField(default=timezone.now)  # agora com valor padrão
    cargo = models.CharField(max_length=20, choices=Cargo.choices, default=Cargo.PRODUCAO)

    def __str__(self):
        return f"{self.username} - {self.cargo}"


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50, unique=True)
    descricao = models.TextField()
    categoria = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Maquina(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    foto = models.ImageField(upload_to='maquinas/', null=True, blank=True)

    def __str__(self):
        return self.nome


class Manutencao(models.Model):
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name='manutencoes')
    data_hora = models.DateTimeField()
    descricao = models.TextField()
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Manutenção {self.maquina.nome} - {self.data_hora}"


class Lote(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField(null=True, blank=True)
    data_inspecao = models.DateTimeField(null=True, blank=True)
    responsavel_inspecao = models.ForeignKey(Funcionario, null=True, blank=True, on_delete=models.SET_NULL)
    status_inspecao = models.CharField(
        max_length=20,
        choices=[('Aprovado', 'Aprovado'), ('Reprovado', 'Reprovado')],
        null=True, blank=True
    )

    def __str__(self):
        return f"Lote {self.codigo}"


class ItemProducao(models.Model):
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()

    def __str__(self):
        return f"Item {self.produto.nome} ({self.lote.codigo})"
