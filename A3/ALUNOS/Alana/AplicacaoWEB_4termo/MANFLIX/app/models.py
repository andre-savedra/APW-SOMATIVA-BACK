from django.db import models
from .user_manager import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class CustomUser(AbstractBaseUser, PermissionsMixin):
   name = models.CharField(max_length=150)
   email = models.EmailField(unique=True)
   cpf = models.CharField(max_length=12, unique=True)
   phone_number = models.CharField(max_length=15, null=True, blank=True, unique=True)
   birth_date = models.DateField(null=True, blank=True)

   is_staff = models.BooleanField(default=False)
   is_active = models.BooleanField(default=True)

   USERNAME_FIELD = "email"
   REQUIRED_FIELDS = ["cpf"]

   # usa o gerenciador criado
   objects = CustomUserManager()

   def __str__(self):
      return self.name


CATEGORIES = [
   ('ROMANCE','ROMANCE'),
   ('DRAMA','DRAMA'),
   ('TERROR','TERROR'),
   ('FICÇÃO','FICÇÃO'),
   ('COMÉDIA','COMÉDIA'),
   ('DOCUMENTÁRIO','DOCUMENTÁRIO'),
   ('AÇÃO','AÇÃO'),
   ('SUSPENSE','SUSPENSE'),
]

class Directors(models.Model):
   name = models.CharField(max_length=400,null=False,blank=False)   

   def __str__(self):
      return self.name

class Movies(models.Model):
   title = models.CharField(max_length=400,null=False,blank=False)
   description = models.CharField(max_length=1000,null=False,blank=False)
   category = models.CharField(max_length=50,choices=CATEGORIES,null=False)
   published_date = models.DateField() 
   photo = models.CharField(max_length=1000,null=False,blank=False)
   directors = models.ManyToManyField(Directors) #Relacionamento (FK), se não fizessemos isso só poderiamos adiconar 1 diretor
   classification = models.IntegerField()

   def __str__(self):
      return self.title

class Plans(models.Model):
   name = models.CharField(max_length=200,null=False,blank=False)
   price = models.DecimalField(max_digits=6,decimal_places=2)

   def __str__(self):
      return self.name

class FavoriteMovies(models.Model):
   movie_FK = models.ForeignKey(Movies, related_name="FavoriteMovies_movie_FK", on_delete=models.CASCADE) #o nome tem que ser unico, por isso para não ter erro colocamos o nome da tabela mais o nome do campo
   user_FK = models.ForeignKey(CustomUser, related_name="FavoriteMovies_user_FK", on_delete=models.CASCADE)
   
   def __str__(self):
      return self.movie_FK.title

  
"""
title = models.CharField(max_length=400, null=False, blank=False)
title é um campo de texto da tabela.

models.CharField define que esse campo é uma string (texto de tamanho limitado).

max_length=400: o campo pode ter no máximo 400 caracteres.

null=False: esse campo não pode ser nulo no banco de dados.

blank=False: esse campo não pode ficar em branco nos formulários do Django Admin ou outros formulários baseados em modelos.

"""