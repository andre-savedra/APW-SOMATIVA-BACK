from django.db import models
from django.contrib.auth.models import User

class Cargo(models.TextChoices):
    MOTORISTA = 'MOTORISTA'
    MECANICO = 'MECÂNICO'
    SUPERVISOR_FROTA = 'SUPERVISOR_FROTA'
    ENGENHEIRO = 'ENGENHEIRO'
    ADMIN = 'ADMIN'


class CategoriaVeiculo(models.TextChoices):
    CARRO = 'CARRO'
    VAN = 'VAN'
    CAMINHAO = 'CAMINHÃO'


class Veiculo(models.Model):
    placa = models.CharField(max_length=100, unique=True)
    modelo = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CategoriaVeiculo.choices)
    data_aquisicao = models.DateField()
    data_ultima_manutencao = models.DateField()

    def __str__(self):
        return self.placa


class Funcionario(models.Model):
    nome = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    matricula = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100)
    cpf = models.CharField(max_length=11)  
    data_contratacao = models.DateField()
    cargo = models.CharField(max_length=20, choices=Cargo.choices)

    def __str__(self):
        return self.nome


class Viagem(models.Model):
    codigo_id = models.CharField(max_length=100, unique=True)
    data_inicio = models.DateField()
    hora_inicio = models.TimeField()
    data_termino = models.DateField()
    hora_termino = models.TimeField()
    destino = models.CharField(max_length=100)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    motorista = models.ForeignKey(Funcionario, on_delete=models.CASCADE, limit_choices_to={'cargo': Cargo.MOTORISTA})
    km = models.PositiveIntegerField()

    def __str__(self):
        return self.codigo_id


class Manutencao(models.Model):
    codigo = models.CharField(max_length=100, unique=True)
    data = models.DateField()
    tipo = models.CharField(max_length=20, choices=[('preventiva', 'Preventiva'), ('corretiva', 'Corretiva')])
    descricao = models.TextField()
    custo = models.DecimalField(max_digits=10, decimal_places=2)
    funcionario_tecnico = models.ForeignKey(Funcionario, on_delete=models.CASCADE, limit_choices_to={'cargo': Cargo.MECANICO})

    def __str__(self):
        return self.codigo
