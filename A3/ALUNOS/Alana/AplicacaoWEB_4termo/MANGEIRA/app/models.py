from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .user_manager import CustomUserManager

Categoria = [
    ('Escritório', 'Escritório'),
    ('Sala de Jantar', 'Sala de Jantar'),
    ('Sala de Estar', 'Sala de Estar'),
    ('Infantil', 'Infantil'),
    ('Quarto', 'Quarto'),
    ('Banheiro', 'Banheiro'),
    ('Jardim e Varanda', 'Jardim e Varanda'),
]

class Produto(models.Model):
    imagem = models.TextField()
    nome = models.CharField(max_length=300)
    estrelas = models.PositiveIntegerField(choices=[(i, i) for i in range(6)])
    quantidade_avaliacões = models.DecimalField(max_digits=6,decimal_places=0)
    preço = models.DecimalField(max_digits=6,decimal_places=2)
    opções_parcelamento = models.CharField(max_length=300)
    categoria = models.CharField(max_length=100,choices=Categoria)
    
    def __str__(self): 
        return self.nome 

class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=12, unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    endereço_completo = models.CharField(max_length=500, default='Endereço não informado')

    #pode acessar tela admin do django ou não
    is_staff = models.BooleanField(default=False)
    #se o usuário está ativo ou não
    is_active = models.BooleanField(default=True)

    #login por email:
    USERNAME_FIELD = "email"

    #o que é obrigatório além do padrão (username, email, password)
    REQUIRED_FIELDS = ["cpf"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

Metodo_pagamento = [
    ('PIX', 'PIX'),
    ('BOLETO', 'BOLETO'),
    ('CartaoDeCredito', 'CartaoDeCredito'),
]

Status = [
    ('EM PROCESSAMENTO', 'EM PROCESSAMENTO'),
    ('PAGAMENTO APROVADO', 'PAGAMENTO APROVADO'),
    ('NOTA FISCAL EMITIDA', 'NOTA FISCAL EMITIDA'),
    ('EM PREPARAÇÃO', 'EM PREPARAÇÃO'),
    ('ENVIADO', 'ENVIADO'),
    ('RECEBIDO', 'RECEBIDO'),
    ('PAGAMENTO REPROVADO', 'PAGAMENTO REPROVADO'),
    ('CANCELADO', 'CANCELADO'),
    ('SOLICITAÇÃO DE DEVOLUÇÃO', 'SOLICITAÇÃO DE DEVOLUÇÃO'),
    ('EM DEVOLUÇÃO', 'EM DEVOLUÇÃO'),
    ('DEVOLUÇÃO CANCELADA', 'DEVOLUÇÃO CANCELADA'),
]

class CartaoDeCredito(models.Model):
    numero_cartao = models.CharField(max_length=16) 
    data_validade = models.CharField(max_length=5)  
    nome_titular = models.CharField(max_length=255)
    codigo_seguranca = models.CharField(max_length=3)  

    def __str__(self):
        return f"Cartão de {self.nome_titular}"

class Pedido(models.Model):
    produto_FK =  models.ManyToManyField(Produto, related_name='pedidos')
    valor_total = models.DecimalField(max_digits=6,decimal_places=2)
    valor_do_desconto = models.DecimalField(max_digits=6,decimal_places=2)
    método_de_pagamento = models.CharField(max_length=100,choices=Metodo_pagamento)
    status = models.CharField(max_length=100,choices=Status)
    código_de_rastreamento = models.CharField(max_length=100, blank=True, null=True)
    user_FK = models.ForeignKey(CustomUser, related_name='UserPlan_user_FK', on_delete=models.CASCADE)
    cartao_de_credito = models.OneToOneField(CartaoDeCredito, null=True, blank=True, on_delete=models.SET_NULL)

    #CALCULAR O VALOR TOTAL AUTOMATICAMENTE
    #AJUSTAR FORMA DE PAGAMENTO QUANDO FOR CARTÃO DE CREDITO

    def __str__(self):
        return f"Pedido de {self.user_FK} - Status: {self.status}"