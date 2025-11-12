from django.db import models


class Lote(models.Model):
    code = models.CharField(max_length=100)
    dthInicio = models.DateTimeField(auto_now_add=True)
    dthFim = models.DateTimeField('Data e hora de fim', null=True, blank=True)
    dtInspecao = models.CharField(max_length=255)
    responsavel = models.ForeignKey('Funcionario', related_name='Lote_usuario_FK', on_delete=models.CASCADE) 
    status = models.BooleanField('Aprovado','Reprovado')
    itens = models.ForeignKey('Item', related_name='Lote_item_FK', on_delete=models.CASCADE)

    def __str__(self):
        return self.name