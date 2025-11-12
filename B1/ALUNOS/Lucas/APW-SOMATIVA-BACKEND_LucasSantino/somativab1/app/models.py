from django.db import models
from django.utils import timezone


class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome


class Funcionario(models.Model):
    class CargoChoices(models.TextChoices):
        MOTORISTA = 'MOTORISTA', 'Motorista'
        MECANICO = 'MECANICO', 'Mecânico'
        SUPERVISOR_FROTA = 'SUPERVISOR_FROTA', 'Supervisor de Frota'
        ENGENHEIRO = 'ENGENHEIRO', 'Engenheiro'
        ADMIN = 'ADMIN', 'Administrador'

    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    data_contratacao = models.DateField()
    cargo = models.CharField(max_length=20, choices=CargoChoices.choices)

    def __str__(self):
        return f"{self.nome} ({self.cargo})"


class Veiculo(models.Model):
    num_placa = models.CharField(max_length=7, unique=True)
    modelo = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='veiculos')
    data_aquisicao = models.DateField()
    data_ultima_manutencao = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.modelo} - {self.num_placa}"


class Viagem(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='viagens')
    motorista = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='viagens')
    data_hora_inicio = models.DateTimeField()
    data_hora_termino = models.DateTimeField(null=True, blank=True)
    destino = models.CharField(max_length=100)
    quilometragem = models.FloatField()

    def __str__(self):
        return f"Viagem {self.id} - {self.veiculo.modelo} ({self.motorista.nome})"


class Manutencao(models.Model):
    class TipoChoices(models.TextChoices):
        PREVENTIVA = 'PREVENTIVA', 'Preventiva'
        CORRETIVA = 'CORRETIVA', 'Corretiva'

    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='manutencoes')
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='manutencoes')
    data = models.DateField(default=timezone.now)
    tipo = models.CharField(max_length=15, choices=TipoChoices.choices)
    descricao = models.TextField()
    custo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.tipo} - {self.veiculo.num_placa} ({self.data})"
