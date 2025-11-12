from django.db import models

class Marca(models.Model):
    name = models.CharField(max_length=150)
    cnpj = models.CharField(max_length=14)
    dataInclusao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name