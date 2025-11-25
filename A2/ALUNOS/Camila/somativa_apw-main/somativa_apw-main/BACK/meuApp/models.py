from django.db import models
from django.contrib.auth.models import User


# --- Cargos ---
class Cargo(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome


# --- Funcionário ---

class Funcionario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=150)
    numero_registro = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    data_contratacao = models.DateField()
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.nome} ({self.cargo.nome})"


# --- Máquina ---
class Maquina(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    foto = models.URLField(blank=True)

    def __str__(self):
        return self.nome


# --- Manutenção ---
class Manutencao(models.Model):
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name="manutencoes")
    data_hora = models.DateTimeField()
    descricao = models.TextField()
    funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.maquina.nome} - {self.data_hora:%d/%m/%Y}"


# --- Produto ---
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50, unique=True)
    descricao = models.TextField()
    categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


# --- Lote ---
class Lote(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    data_inspecao = models.DateTimeField(null=True, blank=True)
    responsavel_inspecao = models.ForeignKey(
        Funcionario, on_delete=models.SET_NULL, null=True, blank=True
    )
    status_inspecao = models.CharField(
        max_length=20, choices=[("Aprovado", "Aprovado"), ("Reprovado", "Reprovado")],
        blank=True
    )

    def __str__(self):
        return f"Lote {self.codigo}"


# --- Itens Lote ---
class ItemLote(models.Model):
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name="itens")
    data_hora = models.DateTimeField()
    maquina = models.ForeignKey(Maquina, on_delete=models.PROTECT)

    def __str__(self):
        return f"Item {self.id} - {self.lote.codigo}"
