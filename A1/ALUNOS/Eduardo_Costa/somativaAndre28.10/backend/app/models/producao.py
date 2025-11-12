from django.db import models

class Producao(models.Model):
   nome = models.CharField(max_length=100)
   lote_FK = models.ForeignKey('Lote', related_name='Producao_lote_FK', on_delete=models.CASCADE)
    
   def __str__(self):
       return self.nome