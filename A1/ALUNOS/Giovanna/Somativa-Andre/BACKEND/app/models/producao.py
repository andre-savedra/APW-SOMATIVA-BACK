from django.db import models


class Status(models.TextChoices):
    Aprovado =  'Aprovado'
    Reprovado = 'Reprovado'

class Producao (models.Model):
    lote_FK= models.ForeignKey('lote',
                               related_name='producao_lote_FK',
                               on_delete=models.SET_NULL,
                               null=True)
    produto_FK=models.ForeignKey('produto',
                                 related_name='Producao_produto_FK',
                                 on_delete=models.SET_NULL,
                               null=True)
    maquina_FK=models.ForeignKey('maquina',
                                 related_name='Producao_maquina_FK',
                                 on_delete=models.SET_NULL,
                               null=True)
    data_producao=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,
                            choices=Status.choices,
                               default=Status.Reprovado)
    funcionario_FK=models.ForeignKey('CustomUser', 
                                     related_name='Prod_funcionario_FK',
                                     on_delete=models.SET_NULL,
                                     null=True)

    def __str__(self):
        return self.lote_FK.codigo

from django.contrib.auth import get_user_model

User = get_user_model()

