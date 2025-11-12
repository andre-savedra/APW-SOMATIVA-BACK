
from django.contrib.auth.models import AbstractUser
from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image

class User(AbstractUser):
    ROLE_CHOICES = [
        ('PRODUCAO', 'Produção'),
        ('CHEFE_PRODUCAO', 'Chefe de Produção'),
        ('INSPECAO', 'Inspeção'),
        ('MANUTENCAO', 'Manutenção'),
        ('ADMIN', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='PRODUCAO')
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    data_contratacao = models.DateField(null=True, blank=True)
    numero_registro = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)
    descricao = models.TextField()
    categoria = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Lote(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField(null=True, blank=True)
    data_inspecao = models.DateTimeField(null=True, blank=True)
    responsavel_inspecao = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        limit_choices_to={'role': 'INSPECAO'}
    )
    status_inspecao = models.CharField(
        max_length=10,
        choices=[('Aprovado', 'Aprovado'), ('Reprovado', 'Reprovado')],
        blank=True,
    )
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="lotes")
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        return f"Lote {self.codigo} - {self.produto.nome}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Gerar QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr_data = f"Lote: {self.codigo}\nProduto: {self.produto.nome}\nInício: {self.data_inicio}"
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, 'PNG')
        
        self.qr_code.save(f'qr_code_{self.codigo}.png', File(buffer), save=False)
        super().save(*args, **kwargs)

class Maquina(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    foto = models.ImageField(upload_to='maquinas/', null=True, blank=True)

    def __str__(self):
        return self.nome

class Manutencao(models.Model):
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name="manutencoes")
    data_hora = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField()
    funcionario = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        limit_choices_to={'role': 'MANUTENCAO'}
    )

    def __str__(self):
        return f"{self.maquina.nome} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

class ItemProduzido(models.Model):
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name="itens")
    data_hora = models.DateTimeField(auto_now_add=True)
    maquina = models.ForeignKey(Maquina, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Item do Lote {self.lote.codigo}"