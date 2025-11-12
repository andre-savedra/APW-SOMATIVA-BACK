from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Campos extras que vamos precisar
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    endereco = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username
