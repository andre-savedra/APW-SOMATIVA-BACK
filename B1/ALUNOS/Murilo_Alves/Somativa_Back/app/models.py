from django.db import models
from django.contrib.auth.models import User

class Funcionario(models.Model):
    CARGOS = [
        ('MOTORISTA', 'Motorista'),
        ('MECANICO', 'Mecânico'),
        ('SUPERVISOR_FROTA', 'Supervisor de Frota'),
        ('ENGENHEIRO', 'Engenheiro'),
        ('ADMIN', 'Admin'),
    ]

    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    data_contratacao = models.DateField()
    cargo = models.CharField(max_length=20, choices=CARGOS)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.nome} ({self.cargo})"

class Veiculo(models.Model):
    CATEGORIAS = [
        ('CARRO', 'Carro'),
        ('VAN', 'Van'),
        ('CAMINHAO', 'Caminhão'),
    ]

    placa = models.CharField(max_length=10, unique=True)
    modelo = models.CharField(max_length=50)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    data_aquisicao = models.DateField()
    data_ultima_manutencao = models.DateField()

    def __str__(self):
        return f"{self.modelo} ({self.placa})"

class Viagem(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=20, unique=True)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    destino = models.CharField(max_length=100)
    quilometragem = models.FloatField()
    motorista = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, related_name='viagens')

    def __str__(self):
        return f"Viagem {self.codigo} - {self.destino}"

class Manutencao(models.Model):
    TIPOS = [
        ('PREVENTIVA', 'Preventiva'),
        ('CORRETIVA', 'Corretiva'),
    ]

    codigo = models.CharField(max_length=20, unique=True)
    data = models.DateField()
    tipo = models.CharField(max_length=15, choices=TIPOS)
    descricao = models.TextField()
    custo = models.DecimalField(max_digits=10, decimal_places=2)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    tecnico = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Manutenção {self.codigo} - {self.tipo}"
