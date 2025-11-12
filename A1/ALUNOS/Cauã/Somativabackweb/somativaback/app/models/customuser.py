from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from datetime import timedelta
from django.utils import timezone


class Cargo(models.TextChoices):
    PRODUCAO = 'PRODUCAO', 'Producao'
    LIDER_PRODUCAO = 'LIDER_PRODUCAO', 'Líder de Producao'
    INSPECAO = 'INSPECAO', 'Inspecao'
    ENGENHARIA = 'ENGENHARIA', 'Engenharia'
    MANUTENCAO = 'MANUTENCAO', 'Manutencao'
    ADMIN = 'ADMIN', 'Administracao'


class FuncionarioManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        required_fields = ['cpf', 'numero_registro', 'data_contratacao', 'cargo', 'nome']

        for field in required_fields:
            if not extra_fields.get(field) and field not in self.model.REQUIRED_FIELDS:
                 raise ValueError(f"O campo '{field}' é obrigatório.")
                 
        if not email or not password:
             raise ValueError("Email e Senha são obrigatórios!")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('cargo', Cargo.ADMIN) 
        
        extra_fields.setdefault('nome', 'Admin')
        extra_fields.setdefault('cpf', '00000000000') 
        extra_fields.setdefault('numero_registro', 'ADMIN001')
        extra_fields.setdefault('data_contratacao', timezone.now().date())


        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Funcionario(AbstractBaseUser, PermissionsMixin):
    nome = models.CharField(max_length=150)
    email = models.EmailField(max_length=255, unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    
    numero_registro = models.CharField(max_length=50, unique=True)
    data_contratacao = models.DateField(null=True) 
    cargo = models.CharField(
        max_length=20,
        choices=Cargo.choices,
        default=Cargo.PRODUCAO
    )
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'cpf', 'numero_registro', 'data_contratacao', 'cargo']

    objects = FuncionarioManager()

    def __str__(self):
        return f"{self.nome} ({self.cargo})"
    
    def get_full_name(self):
        return self.nome
    
    def get_short_name(self):
        return self.nome

