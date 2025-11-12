from django.db import models

class Tokens(models.Model):
    nome = models.CharField(max_length=400, null=False, blank=False)
    data_criacao = models.DateField()
    data_insercao = models.DateField()   
    codigo = models.CharField(max_length=400, null=False, blank=False)
    descricao = models.CharField(max_length=400, null=False, blank=False, verbose_name="descrição")
    valor_conversao = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
      return self.name
    
class Regstros(models.Model):
   data_hora = models.DateField()
   #user_FK = models.ForeignKey(CustomUser, related_name="FavoriteMovies_movie_FK", on_delete=models.CASCADE)
   token_FK = models.ManyToManyField(Tokens)
   destino = models.CharField(max_length=400, null=False, blank=False)
   quantidade = models.IntegerField()

class Jogadas(models.Model):
   resultado = models.CharField(max_length=400, null=False, blank=False)
   quantia = models.DecimalField(max_digits=10,decimal_places=2)
