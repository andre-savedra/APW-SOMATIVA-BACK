from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    descricao = models.CharField(max_length=255)
    categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.nome