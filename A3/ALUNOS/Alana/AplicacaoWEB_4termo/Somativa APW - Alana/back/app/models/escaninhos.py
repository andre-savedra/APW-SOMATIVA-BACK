from django.db import models

class Escaninhos(models.Model):
    cod = models.CharField(max_length=150)
    setor_FK = models.ForeignKey('Setor', 
                                related_name='Escaninhos_setor_FK',
                                on_delete=models.SET_NULL,
                                null=True)
    produto_FK = models.ForeignKey('Produto', 
                                related_name='Escaninhos_produto_FK',
                                on_delete=models.SET_NULL,
                                null=True)
    quantidade = models.CharField(max_length=150)

    def __str__(self):
        return self.cod