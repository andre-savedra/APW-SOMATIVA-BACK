from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Hospede(models.Model):
    nome_inteiro = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    data_de_registro = models.DateField(default=timezone.now)
    nacionalidade = models.CharField(max_length=100)


    def __str__(self):
        return f"{self.nome_inteiro} ({self.cpf})"


class Acomodacao(models.Model):
    tipos_acomodacao = [
        ("STANDARD", "Standard"),
        ("SUITE", "Suíte"),
        ("MASTER", "Master"),
    ]
    status_acomodacao = [
        ("DISPONIVEL", "Disponível"),
        ("OCUPADA", "Ocupada"),
        ("MANUTENCAO", "Em manutenção"),
    ]


    numero = models.CharField(max_length=20, unique=True)
    tipo = models.CharField(max_length=20, choices=tipos_acomodacao)
    capacidade_maxima = models.PositiveIntegerField()
    avaliacao_diaria = models.DecimalField(max_digits=10, decimal_places=2)
    data_ultimaLimpeza = models.DateField()
    status = models.CharField(max_length=20, choices=status_acomodacao, default="DISPONIVEL")


    def __str__(self):
        return f"Acomodação {self.numero} - {self.tipo}"


class EmpregadoManager(BaseUserManager):
    def create_user(self, registro, nome, cargo, password=None, **extra_fields):
        if not registro:
            raise ValueError("O registro deve ser informado")
        user = self.model(registro=registro, nome=nome, cargo=cargo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, registro, nome, cargo, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(registro, nome, cargo, password, **extra_fields)

class Empregado(AbstractBaseUser, PermissionsMixin):
    cargos_tipo = [
        ("RECEPCAO", "Recepção"),
        ("GOVERNANCA", "Governança"),
        ("MANUTENCAO", "Manutenção"),
        ("GERENCIA", "Gerência"),
        ("ADMIN", "Admin"),
    ]

    nome = models.CharField(max_length=200)
    registro = models.CharField(max_length=50, unique=True)
    cargo = models.CharField(max_length=20, choices=cargos_tipo)
    data_contratacao = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "registro"
    REQUIRED_FIELDS = ["nome", "cargo"]

    objects = EmpregadoManager()
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='empregado_set',  # evita conflito
        blank=True,
        help_text='Grupos de usuários.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='empregado_set',  # evita conflito
        blank=True,
        help_text='Permissões do usuário.',
        verbose_name='user permissions'
    )


class Limpeza(models.Model):

    acomodacao = models.ForeignKey(Acomodacao, on_delete=models.CASCADE)
    empregado = models.ForeignKey(Empregado, on_delete=models.SET_NULL, null=True, blank=True)
    ultima_vez_limpo = models.DateTimeField(default=timezone.now)
    nota = models.TextField(blank=True)

    def __str__(self):
        return f"Limpeza {self.acomodacao.numero} em {self.ultima_vez_limpo:%Y-%m-%d %H:%M}"


class Manutencoes(models.Model):
    acomodacao = models.ForeignKey(Acomodacao, on_delete=models.CASCADE)
    empregado = models.ForeignKey(Empregado, on_delete=models.SET_NULL, null=True)
    descricao = models.TextField()
    data = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"Manutenção {self.acomodacao.numero} @ {self.criado:%Y-%m-%d}"


class Reservas(models.Model):
    status_reservas = [
        ("ATIVA", "Ativa"),
        ("FINALIZADA", "Finalizada"),
        ("CANCELADA", "Cancelada"),
    ]
    codigo = models.CharField(max_length=50, unique=True)
    hospede = models.ForeignKey(Hospede, on_delete=models.CASCADE)
    acomodacao = models.ForeignKey(Acomodacao, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=status_reservas, default="ATIVA")
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva {self.codigo} - {self.hospede.nome_inteiro} ({self.acomodacao.numero})"
    


# class CustomUser(AbstractUser):
#     CARGOS = [
#         ('RECEPCAO', 'Recepção'),
#         ('GOVERNANCA', 'Governança'),
#         ('MANUTENCAO', 'Manutenção'),
#         ('GERENCIA', 'Gerência'),
#         ('ADMIN', 'Administração'),
#     ]
#     cargo = models.CharField(max_length=20, choices=CARGOS, default='RECEPCAO')

#     def __str__(self):
#         return f"{self.username} ({self.cargo})"