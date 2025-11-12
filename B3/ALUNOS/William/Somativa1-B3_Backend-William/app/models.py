from django.db import models
from django.utils import timezone

class Guest(models.Model):
    nome_completo = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=30, blank=True)
    data_cadastro = models.DateTimeField(default=timezone.now)
    nacionalidade = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome_completo} ({self.cpf})"


class Accommodation(models.Model):
    TYPE_CHOICES = [
        ('standard', 'Standard'),
        ('suite', 'Suíte'),
        ('master', 'Master'),
    ]
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('ocupada', 'Ocupada'),
        ('manutencao', 'Em manutenção'),
    ]

    numero = models.CharField(max_length=20, unique=True)
    tipo = models.CharField(max_length=20, choices=TYPE_CHOICES)
    capacidade = models.PositiveIntegerField()
    valor_diaria = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel')
    data_ultima_limpeza = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Acom. {self.numero} - {self.tipo}"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ]

    codigo = models.CharField(max_length=50, unique=True)
    hospede = models.ForeignKey(Guest, related_name='reservas', on_delete=models.PROTECT)
    acomodacao = models.ForeignKey(Accommodation, related_name='reservas', on_delete=models.PROTECT)
    data_checkin = models.DateField()
    data_checkout = models.DateField()
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativa')

    def __str__(self):
        return f"Reserva {self.codigo} - {self.hospede.nome_completo}"


class Role(models.TextChoices):
    RECEPCAO = 'RECEPCAO', 'Recepção'
    GOVERNANCA = 'GOVERNANCA', 'Governança'
    MANUTENCAO = 'MANUTENCAO', 'Manutenção'
    GERENCIA = 'GERENCIA', 'Gerência'
    ADMIN = 'ADMIN', 'Admin'


class Employee(models.Model):
    nome = models.CharField(max_length=200)
    matricula = models.CharField(max_length=50, unique=True)
    cargo = models.CharField(max_length=20, choices=Role.choices)
    data_contratacao = models.DateField()

    def __str__(self):
        return f"{self.nome} ({self.matricula})"


class CleaningRecord(models.Model):
    acomodacao = models.ForeignKey(Accommodation, related_name='limpezas', on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Employee, related_name='limpezas', on_delete=models.SET_NULL, null=True)
    data_limpeza = models.DateField(default=timezone.now)
    observacao = models.TextField(blank=True)

    class Meta:
        ordering = ['-data_limpeza']

    def __str__(self):
        return f"Limpeza {self.acomodacao.numero} em {self.data_limpeza}"


class MaintenanceRecord(models.Model):
    acomodacao = models.ForeignKey(Accommodation, related_name='manutencoes', on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Employee, related_name='manutencoes', on_delete=models.SET_NULL, null=True)
    data_manutencao = models.DateTimeField(default=timezone.now)
    descricao = models.TextField()

    class Meta:
        ordering = ['-data_manutencao']

    def __str__(self):
        return f"Manutenção {self.acomodacao.numero} em {self.data_manutencao}"
