from django.db import models

class Maquina (models.Model):
    nome= models.CharField(max_length=150)
    descricao= models.CharField(max_length=500)
    data_manutencao= models.DateTimeField(auto_now_add=True)
    funcionario_FK=models.ForeignKey('CustomUser', 
                                     related_name='Maquina_funcionario_FK',
                                     on_delete=models.SET_NULL,
                                     null=True)
    
    def __str__(self):
        return self.nome