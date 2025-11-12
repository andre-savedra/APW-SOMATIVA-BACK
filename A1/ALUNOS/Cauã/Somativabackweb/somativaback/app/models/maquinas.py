from django.db import models
from django.utils import timezone
from datetime import timedelta
from .customuser import Funcionario


class Maquina(models.Model):
    codigo_identificador = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    ultima_data_manutencao = models.DateTimeField(null=True, blank=True) 
    responsavel_manutencao = models.ForeignKey(
        Funcionario,
        on_delete=models.SET_NULL,
        null=True,
        related_name='maquinas_mantidas'
    )
    
    @property
    def precisa_manutencao(self):
        if self.ultima_data_manutencao is None:
            return True 
        
        tres_meses_atras = timezone.now() - timedelta(days=90)
        return self.ultima_data_manutencao < tres_meses_atras

    def __str__(self):
        return self.nome