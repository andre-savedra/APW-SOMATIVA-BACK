from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class FuncionarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O usuário precisa de um e-mail válido.')
        email = self.normalize_email(email)
        extra_fields.setdefault('cargo', 'RECEPCAO')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('cargo', 'ADMIN')
        return self.create_user(email, password, **extra_fields)


class Funcionario(AbstractBaseUser, PermissionsMixin):
    class CargoChoices(models.TextChoices):
        RECEPCAO = 'RECEPCAO', 'Recepção'
        GOVERNANCA = 'GOVERNANCA', 'Governança'
        MANUTENCAO = 'MANUTENCAO', 'Manutenção'
        GERENCIA = 'GERENCIA', 'Gerência'
        ADMIN = 'ADMIN', 'Administração'

    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    matricula = models.CharField(max_length=20, blank=True, null=True)
    cargo = models.CharField(max_length=20, choices=CargoChoices.choices, default='RECEPCAO')
    data_contratacao = models.DateField(default=timezone.now, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = FuncionarioManager()

    def __str__(self):
        return f"{self.email} ({self.cargo})"


class Hospede(models.Model):
    nome_completo = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    data_cadastro = models.DateField(default=timezone.now)
    nacionalidade = models.CharField(max_length=50)

    def __str__(self):
        return self.nome_completo


class Acomodacao(models.Model):
    class TipoChoices(models.TextChoices):
        STANDARD = 'STANDARD', 'Standard'
        SUITE = 'SUITE', 'Suíte'
        MASTER = 'MASTER', 'Master'

    class StatusChoices(models.TextChoices):
        DISPONIVEL = 'DISPONIVEL', 'Disponível'
        OCUPADA = 'OCUPADA', 'Ocupada'
        MANUTENCAO = 'MANUTENCAO', 'Em manutenção'

    numero = models.IntegerField(unique=True)
    tipo = models.CharField(max_length=20, choices=TipoChoices.choices)
    capacidade_maxima = models.IntegerField()
    valor_diaria = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.DISPONIVEL)
    data_ultima_limpeza = models.DateField(null=True, blank=True)
    funcionario_responsavel = models.ForeignKey(Funcionario, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Acomodação {self.numero} - {self.tipo}"


class Reserva(models.Model):
    class StatusChoices(models.TextChoices):
        ATIVA = 'ATIVA', 'Ativa'
        FINALIZADA = 'FINALIZADA', 'Finalizada'
        CANCELADA = 'CANCELADA', 'Cancelada'

    codigo = models.CharField(max_length=10, unique=True)
    hospede = models.ForeignKey(Hospede, on_delete=models.CASCADE)
    acomodacao = models.ForeignKey(Acomodacao, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=15, choices=StatusChoices.choices, default=StatusChoices.ATIVA)

    def save(self, *args, **kwargs):
        dias = (self.check_out - self.check_in).days
        diaria = self.acomodacao.valor_diaria if self.acomodacao else 0
        self.valor_total = dias * diaria
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva {self.codigo} ({self.status})"



class Manutencao(models.Model):
    acomodacao = models.ForeignKey(Acomodacao, on_delete=models.CASCADE, related_name='manutencoes')
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    descricao = models.TextField()
    data = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Manutenção {self.id} - {self.acomodacao.numero}"
