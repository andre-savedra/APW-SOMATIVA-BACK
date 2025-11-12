from django.db import models

class Produto(models.Model):
    name = models.CharField(max_length=150)
    codeRegistro = models.CharField(max_length=50)
    codeBarras = models.CharField(max_length=50)
    categoria_FK = models.ForeignKey('Categoria', 
                                related_name='Produto_categoria_FK',
                                on_delete=models.SET_NULL,
                                null=True)
    marca_FK = models.ForeignKey('Marca', 
                                related_name='Produto_marca_FK',
                                on_delete=models.SET_NULL,
                                null=True)
    dataCadastro = models.DateTimeField(auto_now_add=True)
    custo = models.DecimalField(max_digits=10, decimal_places=2)
    valorVenda = models.DecimalField(max_digits=10, decimal_places=2)
    promocao = models.BooleanField(default=False)



    def __str__(self):
        return self.name
    






