from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

CATEGORIES = [
    ('PRODUCTION', 'Máquina de Produção'),
    ('AUTOMATED_MACHINE', 'Máquina Automatizada'),
    ('MAINTENANCE_MACHINE', 'Máquina de Manutenção'),
]

MAQUINA_CATEGORIES = [
    ('CORTE', 'Máquina de Corte'),
    ('MONTAGEM', 'Máquina de Montagem'),
    ('INSPECAO', 'Máquina de Inspeção'),
    ('EMBALAGEM', 'Máquina de Embalagem'),
    ('MANUTENCAO', 'Máquina de Manutenção'),
]


STATUS = [
    ('APPROVED', 'Aprovado'),
    ('REPROVED', 'Reprovado'),
]

CARGOS = [
    ('PRODUCAO', 'Produção'),
    ('CHEFE_PRODUCAO', 'Chefe de Produção'),
    ('INSPECAO', 'Inspeção'),
    ('MANUTENCAO', 'Manutenção'),
    ('ADMIN', 'Admin'),
]

class CustomUserManager(BaseUserManager):
    def create_user(self, email, cpf, password=None, **extra_fields):
        if not email:
            raise ValueError("O campo email é obrigatório")
        if not cpf:
            raise ValueError("O campo CPF é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, cpf=cpf, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, cpf, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, cpf, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=12, unique=True)
    numero_registro = models.CharField(max_length=20, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    data_contratacao = models.DateField(null=True, blank=True)
    cargo = models.CharField(max_length=50, choices=CARGOS, default='PRODUCAO')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["cpf"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Produto(models.Model):
    nome = models.CharField(max_length=300, default="Produto sem nome")
    codigo = models.IntegerField(default=0)
    descricao = models.CharField(max_length=300)
    categoria = models.CharField(max_length=100, choices=CATEGORIES)

    def __str__(self):
        return self.nome

class Maquina(models.Model):
    codigo = models.IntegerField(default=0)
    foto = models.TextField(default="sem foto")
    nome = models.CharField(max_length=250, default="Máquina sem nome")
    descricao = models.CharField(max_length=250)
    categoria = models.CharField(max_length=100, choices=MAQUINA_CATEGORIES, default='CONVENCIONAL')

    def __str__(self):
        return self.nome

class Manutencao(models.Model):
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name='manutencoes')
    data_hora = models.DateTimeField(default=timezone.now)
    descricao = models.TextField()
    responsavel = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        nome_maquina = self.maquina.nome if self.maquina else 'Máquina indefinida'
        return f"{nome_maquina} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

class Lote(models.Model):
    codigo = models.IntegerField(default=0)
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True, blank=True)
    data_inicio = models.DateTimeField(default=timezone.now)
    data_final = models.DateTimeField(default=timezone.now)
    data_inspecao = models.DateTimeField(default=timezone.now)
    qr_code = models.TextField()
    responsavel = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS, default="APPROVED")

    def __str__(self):
        return f"Lote {self.codigo}"


class ItensLote(models.Model):
    data_hora = models.DateTimeField(default=timezone.now)
    maquina = models.ForeignKey(Maquina, on_delete=models.SET_NULL, null=True, blank=True)
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name="itens")

    def __str__(self):
        nome_maquina = self.maquina.nome if self.maquina else 'Máquina indefinida'
        return f"{nome_maquina} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"
