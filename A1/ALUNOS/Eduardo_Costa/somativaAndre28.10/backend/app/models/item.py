from django.db import models

class Item(models.Model):
    nome = models.CharField(max_length=100)
    dthItem = models.DateTimeField()
    identificacaoMaquina = models.ForeignKey('Maquina', related_name='Item_maquina_FK', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
