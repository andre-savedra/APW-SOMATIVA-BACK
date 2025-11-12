from django.db import models



class Produto (models.Model):
    nome =models.CharField(max_length=150)
    codigo =models.CharField(max_length=30)
    descricao=models.CharField(max_length=500)
    categoria_FK =models.ForeignKey('Categoria', related_name=
                                    'Produto_categoria_FK', on_delete=models.SET_NULL,
                                    null=True)
    
    def __str__(self):
        return self.nome