from django.db import models
from accounts.models import User


# Categoria
class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

# Produto
class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagem_url = models.URLField()
    estrelas_media = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_avaliacoes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nome

# Peças do Produto
class Peca(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='pecas')
    nome = models.CharField(max_length=100)
    medidas = models.CharField(max_length=100)
    peso = models.DecimalField(max_digits=6, decimal_places=2)  # kg

    def __str__(self):
        return f"{self.produto.nome} - {self.nome}"

# Avaliação de Produto
class Avaliacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='avaliacoes')
    item = models.ForeignKey('orders.ItemPedido', on_delete=models.CASCADE)  # <-- aqui usa string
    nota = models.PositiveSmallIntegerField()  # 1 a 5
    comentario = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
