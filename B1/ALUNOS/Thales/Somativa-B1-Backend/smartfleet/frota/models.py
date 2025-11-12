import uuid
from django.db import models
from django.contrib.auth.models import User

class Funcionario(models.Model):
    
  
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='funcionario',
        null=True,  
        blank=True  
    )


    class Cargos(models.TextChoices):
        MOTORISTA = 'MOTORISTA', 'Motorista'
        MECANICO = 'MECANICO', 'Mecânico'
        SUPERVISOR_FROTA = 'SUPERVISOR_FROTA', 'Supervisor de Frota'
        ENGENHEIRO = 'ENGENHEIRO', 'Engenheiro'
        ADMIN = 'ADMIN', 'Admin'

    nome = models.CharField(max_length=80)
    matricula = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    data_contratacao = models.DateField()
    cargo = models.CharField(max_length=20, choices=Cargos.choices)

    def __str__(self):
        return f"{self.nome} ({self.matricula}) - {self.get_cargo_display()}"


class CategoriaVeiculo(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome


class Veiculo(models.Model):

    placa = models.CharField(max_length=10, unique=True)
    modelo = models.CharField(max_length=50)
    categoria = models.ForeignKey(
        CategoriaVeiculo,
        on_delete=models.PROTECT, 
        related_name='veiculos'
    )
    data_aquisicao = models.DateField()
    data_ultima_manutencao = models.DateField(null=True, blank=True) 

    def __str__(self):
        return f"{self.modelo} - {self.placa}"


class Viagem(models.Model):
   
    codigo_identificador = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, unique=True)
    
   
    veiculo = models.ForeignKey(
        Veiculo, 
        on_delete=models.PROTECT,  
        related_name='viagens'
    )
    
    data_hora_inicio = models.DateTimeField()
    data_hora_termino = models.DateTimeField(null=True, blank=True) 
    destino = models.CharField(max_length=100)
    quilometragem = models.DecimalField(max_digits=10, decimal_places=2)

    
    motorista = models.ForeignKey(
        Funcionario, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='viagens_motorista',
        limit_choices_to={'cargo': Funcionario.Cargos.MOTORISTA}
    )

    def __str__(self):
        return f"Viagem {self.codigo_identificador} - {self.veiculo.placa}"

class Manutencao(models.Model):

    class TiposManutencao(models.TextChoices):
        PREVENTIVA = 'PREVENTIVA', 'Preventiva'
        CORRETIVA = 'CORRETIVA', 'Corretiva'


    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.CASCADE, 
        related_name='manutencoes'
    )

    codigo = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, unique=True)
    data = models.DateField()
    tipo = models.CharField(max_length=10, choices=TiposManutencao.choices)
    descricao = models.TextField()
    custo = models.DecimalField(max_digits=10, decimal_places=2)

    tecnico = models.ForeignKey(
        Funcionario, 
        on_delete=models.SET_NULL,
        null=True,
        related_name='manutencoes_tecnico',
        limit_choices_to={'cargo': Funcionario.Cargos.MECANICO}
    )

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.veiculo.placa} ({self.data})"