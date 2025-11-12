from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

CARGO_CHOICES = [
    ('Producao', 'producao'),
    ('Lider_producao', 'lider de producao'),
    ('Inspecao', 'inspecao'),
    ('Engenharia', 'engenharia'),
    ('Tecnico', 'tecnico'),
    ('Manutencao', 'manutencao'),
    ('Admin', 'admin'),

]

class VerificationUser(BaseUserManager):
    def create_user(self, email, nome, numero_registro, cpf, cargo, dt_contratacao, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        funcionario = self.model(email=email, nome=nome, numero_registro=numero_registro, cpf=cpf, cargo=cargo, dt_contratacao=dt_contratacao)
        funcionario.set_password(password)
        funcionario.save(using=self._db)
        return funcionario

    def create_superuser(self, email, nome, numero_registro, cpf, cargo, dt_contratacao, password):
        funcionario = self.create_user(email, nome, numero_registro, cpf, cargo, dt_contratacao, password)
        funcionario.is_admin = True
        funcionario.is_staff = True
        funcionario.is_superuser = True
        funcionario.save(using=self._db)
        return funcionario

class Funcionario(AbstractBaseUser, PermissionsMixin):
    nome = models.CharField(max_length=100)
    numero_registro = models.CharField(max_length=50, unique=True)
    cargo = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=11, unique=True) 
    dt_contratacao = models.DateField() 
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    cargo = models.CharField(max_length=50, choices=CARGO_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'numero_registro', 'cpf', 'cargo', 'dt_contratacao']

    objects = VerificationUser()

    def __str__(self):
        return self.nome