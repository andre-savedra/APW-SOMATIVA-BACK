from django.db import models
from django.contrib.auth.models import User 

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True, help_text="Nome da categoria")
    def __str__(self):
        return self.nome

class Marca(models.Model):
    nome = models.CharField(max_length=100, unique=True, help_text="Nome da marca/fabricante")
    cnpj = models.CharField(max_length=18, unique=True, help_text="CNPJ")
    data_inclusao = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.nome

class Setor(models.Model):
    letra = models.CharField(max_length=2, unique=True, help_text="Letra ou código do setor")
    def __str__(self):
        return f"Setor {self.letra}"

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    codigo_barras_numerico = models.CharField(max_length=100, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='produtos')
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, related_name='produtos')
    data_cadastro = models.DateField(auto_now_add=True)
    custo = models.DecimalField(max_digits=10, decimal_places=2)
    valor_venda = models.DecimalField(max_digits=10, decimal_places=2)
    informacoes_adicionais = models.TextField(blank=True, null=True)
    em_promocao = models.BooleanField(default=False)

    class Meta:
        ordering = ['nome']
    def __str__(self):
        return self.nome

class Escaninho(models.Model):
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, related_name='escaninhos')
    codigo_escaninho = models.CharField(max_length=50, unique=True)
    localizacao = models.CharField(max_length=255, blank=True, null=True)
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, blank=True, null=True, related_name='localizacao_estoque')
    quantidade = models.PositiveIntegerField(default=0)

    def __str__(self):
        if self.produto:
            return f"{self.codigo_escaninho} (Setor {self.setor.letra}) - {self.quantidade}x {self.produto.nome}"
        return f"{self.codigo_escaninho} (Setor {self.setor.letra}) - Vazio"