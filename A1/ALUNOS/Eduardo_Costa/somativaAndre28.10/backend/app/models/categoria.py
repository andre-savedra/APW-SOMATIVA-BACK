from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=150)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'