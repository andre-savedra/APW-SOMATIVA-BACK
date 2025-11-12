from django.db import models
from .brand import Marca
from .category import Categoria
from .shelf import Escaninho

class Produto(models.Model):
    nome = models.CharField(max_length=150)
    codigo = models.CharField(max_length=50, unique=True)
    codigo_barras = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    promocao = models.BooleanField(default=False)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='produtos')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='produtos')
    escaninho = models.ForeignKey(Escaninho, on_delete=models.CASCADE, related_name='produtos')

    def __str__(self):
        return self.nome