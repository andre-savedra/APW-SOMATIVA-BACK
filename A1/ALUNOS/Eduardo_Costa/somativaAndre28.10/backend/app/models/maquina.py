from django.db import models

class Maquina(models.Model):
    code = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=255)
    ultima_manutencao = models.DateTimeField()
    responsavel = models.ForeignKey('Funcionario', related_name='Maquina_usuario_FK', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
   