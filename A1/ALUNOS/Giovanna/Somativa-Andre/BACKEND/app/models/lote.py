from django.db import models


class Lote (models.Model):
    codigo = models.CharField(max_length=50)
    data_inicio=models.DateTimeField(auto_now_add=True)
    data_fim = models.DateTimeField(auto_now_add=True)
    data_inspecao= models.DateTimeField(auto_now_add=True)
    funcionario_FK=models.ForeignKey('CustomUser', 
                                     related_name='Lote_funcionario_FK',
                                     on_delete=models.SET_NULL,
                                     null=True)
    
    def __str__(self):
        return self.codigo