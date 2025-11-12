from django.db import models
from .sector import Setor

class Escaninho(models.Model):
    nome = models.CharField(max_length=100)
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, related_name='escaninhos')

    def __str__(self):
        return f"{self.nome} - {self.setor.nome}"