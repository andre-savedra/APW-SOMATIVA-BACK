from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Cargo(models.TextChoices):
    PRODUCAO = 'PRODUCAO', 'Produção'
    LIDER_PRODUCAO = 'LIDER_PRODUCAO', 'Líder de Produção'
    INSPECAO = 'INSPECAO', 'Inspeção'
    MANUTENCAO = 'MANUTENCAO', 'Manutenção'
    ADMIN = 'ADMIN', 'Admin'


class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=150)
    codigo = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='produtos')

    def __str__(self) -> str:
        return f"{self.nome} ({self.codigo})"


class Funcionario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='funcionario')
    nome = models.CharField(max_length=150)
    registro = models.CharField(max_length=50, unique=True)
    email = models.EmailField()
    cpf = models.CharField(max_length=14, unique=True)
    data_contratacao = models.DateField()
    cargo = models.CharField(max_length=20, choices=Cargo.choices)

    def __str__(self) -> str:
        return f"{self.nome} - {self.cargo}"


class Maquina(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    foto = models.URLField(blank=True, null=True)
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.nome} ({self.codigo})"


class Manutencao(models.Model):
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name='manutencoes')
    data_hora = models.DateTimeField(default=timezone.now)
    descricao = models.TextField()
    funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT, related_name='manutencoes_executadas')

    class Meta:
        ordering = ['-data_hora']

    def __str__(self) -> str:
        return f"{self.maquina.codigo} - {self.data_hora:%Y-%m-%d %H:%M}"


class InspecaoStatus(models.TextChoices):
    APROVADO = 'APROVADO', 'Aprovado'
    REPROVADO = 'REPROVADO', 'Reprovado'


class Lote(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='lotes')
    inicio = models.DateTimeField()
    fim = models.DateTimeField(null=True, blank=True)
    data_inspecao = models.DateTimeField(null=True, blank=True)
    inspetor = models.ForeignKey(
        Funcionario, on_delete=models.PROTECT, null=True, blank=True, related_name='lotes_inspecionados'
    )
    status_inspecao = models.CharField(
        max_length=10, choices=InspecaoStatus.choices, null=True, blank=True
    )

    class Meta:
        ordering = ['-inicio']

    def __str__(self) -> str:
        return f"Lote {self.codigo} - {self.produto.nome}"


class ItemProducao(models.Model):
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name='itens')
    data_hora = models.DateTimeField(default=timezone.now)
    maquina = models.ForeignKey(Maquina, on_delete=models.PROTECT, related_name='itens_produzidos')

    class Meta:
        ordering = ['data_hora']

    def __str__(self) -> str:
        return f"Item {self.lote.codigo} @ {self.data_hora:%Y-%m-%d %H:%M}"


