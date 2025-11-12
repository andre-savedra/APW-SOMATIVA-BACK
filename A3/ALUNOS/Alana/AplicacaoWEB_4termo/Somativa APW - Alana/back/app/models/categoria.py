from django.db import models

class Categoria(models.Model):
    name = models.CharField(max_length=150)
    dataRegistro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    