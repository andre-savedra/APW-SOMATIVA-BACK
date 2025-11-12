from django.db import models
from .customuser import Funcionario, Cargo 


class Lote(models.Model):
    STATUS_INSPECAO_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('APROVADO', 'Aprovado'), # Status (aprovado/reprovado)
        ('REPROVADO', 'Reprovado'),
    ]

    codigo = models.CharField(max_length=50, unique=True)
    data_hora_inicio = models.DateTimeField() # data e hora inicio
    data_hora_finalizacao = models.DateTimeField(blank=True, null=True) # data e hora fim
    data_inspecao = models.DateTimeField(blank=True, null=True)
    
    # Responsável pela inspeção (fk funcionario)
    responsavel_inspecao = models.ForeignKey(
        Funcionario,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'cargo': Cargo.INSPECAO},
        related_name='lotes_inspecionados'
    )
    
    status_inspecao = models.CharField(
        max_length=10,
        choices=STATUS_INSPECAO_CHOICES,
        default='PENDENTE'
    )

    def __str__(self):
        return self.codigo