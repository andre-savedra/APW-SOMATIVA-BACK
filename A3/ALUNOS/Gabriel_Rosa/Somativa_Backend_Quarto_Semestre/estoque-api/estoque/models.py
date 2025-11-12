from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import re

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    data_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome

class Marca(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    cnpj = models.CharField(
        max_length=18, 
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
                message='CNPJ deve estar no formato XX.XXX.XXX/XXXX-XX'
            )
        ]
    )
    data_inclusao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome

class Setor(models.Model):
    nome = models.CharField(
        max_length=1, 
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Z]$',
                message='Setor deve ser uma única letra maiúscula (A-Z)'
            )
        ]
    )
    descricao = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Setor"
        verbose_name_plural = "Setores"
        ordering = ['nome']
    
    def __str__(self):
        return f"Setor {self.nome}"

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    codigo_registro = models.CharField(max_length=50, unique=True)
    codigo_barras = models.CharField(
        max_length=13, 
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{8,13}$',
                message='Código de barras deve conter apenas números (8-13 dígitos)'
            )
        ]
    )
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.PROTECT,
        related_name='produtos'
    )
    marca = models.ForeignKey(
        Marca, 
        on_delete=models.PROTECT,
        related_name='produtos'
    )
    data_cadastro = models.DateTimeField(auto_now_add=True)
    custo = models.DecimalField(max_digits=10, decimal_places=2)
    valor_venda = models.DecimalField(max_digits=10, decimal_places=2)
    informacoes_adicionais = models.TextField(blank=True, null=True)
    em_promocao = models.BooleanField(default=False)
    
    # Campos para auditoria
    criado_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='produtos_criados'
    )
    promocao_alterada_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='promocoes_alteradas'
    )
    data_promocao = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['-data_cadastro']
        indexes = [
            models.Index(fields=['codigo_barras']),
            models.Index(fields=['em_promocao']),
            models.Index(fields=['data_cadastro']),
            models.Index(fields=['valor_venda']),
        ]
    
    def __str__(self):
        return f"{self.nome} - {self.codigo_registro}"
    
    @property
    def margem_lucro(self):
        if self.custo > 0:
            return ((self.valor_venda - self.custo) / self.custo) * 100
        return 0

class Escaninho(models.Model):
    codigo = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='Código do escaninho deve conter apenas números'
            )
        ]
    )
    setor = models.ForeignKey(
        Setor, 
        on_delete=models.CASCADE,
        related_name='escaninhos'
    )
    produto = models.ForeignKey(
        Produto, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='escaninhos'
    )
    quantidade = models.PositiveIntegerField(default=0)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Escaninho"
        verbose_name_plural = "Escaninhos"
        ordering = ['setor__nome', 'codigo']
        unique_together = ['setor', 'codigo']
    
    def __str__(self):
        produto_info = f" - {self.produto.nome}" if self.produto else " - Vazio"
        return f"Setor {self.setor.nome} - Escaninho {self.codigo}{produto_info}"
    
    def save(self, *args, **kwargs):
        # Se não tem produto, quantidade deve ser 0
        if not self.produto:
            self.quantidade = 0
        super().save(*args, **kwargs)