from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    CARGO_CHOICES = [
        ('RECEPCAO', 'Recepção'),
        ('GOVERNANCA', 'Governança'),
        ('MANUTENCAO', 'Manutenção'),
        ('GERENCIA', 'Gerência'),
        ('ADMIN', 'Admin'),
    ]
    matricula = models.CharField(max_length=50, unique=True)
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES)
    data_contratacao = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.cargo})"