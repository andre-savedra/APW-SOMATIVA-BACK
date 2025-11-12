from django.db import models
from accounts.models import User
from store.models import Produto

# Pedido
class Pedido(models.Model):
    STATUS_CHOICES = [
        ('EM_PROCESSAMENTO', 'Em processamento'),
        ('PAGAMENTO_APROVADO', 'Pagamento aprovado'),
        ('NOTA_FISCAL_EMITIDA', 'Nota fiscal emitida'),
        ('EM_PREPARACAO', 'Em preparação'),
        ('ENVIADO', 'Enviado'),
        ('RECEBIDO', 'Recebido'),
        ('PAGAMENTO_REPROVADO', 'Pagamento reprovado'),
        ('CANCELADO', 'Cancelado'),
        ('SOLICITACAO_DEVOLUCAO', 'Solicitação de devolução'),
        ('EM_DEVOLUCAO', 'Em devolução'),
        ('DEVOLVIDO', 'Devolvido'),
        ('DEVOLUCAO_CANCELADA', 'Devolução cancelada'),
    ]
    METODO_PAGAMENTO = [
        ('PIX', 'PIX'),
        ('BOLETO', 'Boleto'),
        ('CARTAO', 'Cartão de crédito'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='EM_PROCESSAMENTO')
    metodo_pagamento = models.CharField(max_length=10, choices=METODO_PAGAMENTO)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    valor_desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    codigo_rastreamento = models.CharField(max_length=50, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

# Itens do Pedido (Carrinho)
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

# Cartão de Crédito (somente se método CARTÃO)
class CartaoCredito(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='cartao')
    numero = models.CharField(max_length=16)
    nome_titular = models.CharField(max_length=100)
    validade = models.CharField(max_length=5)  # MM/AA
    codigo = models.CharField(max_length=4)

# Devolução
class Devolucao(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemPedido, on_delete=models.CASCADE)
    motivo = models.TextField()
    data_solicitacao = models.DateTimeField(auto_now_add=True)
