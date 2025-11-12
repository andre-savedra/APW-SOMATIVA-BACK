from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .user_manager import CustomUserManager

CATEGORIES = [
    ('HORROR','Terror'),
    ('COMEDY', 'Comédia'),
    ('FICCTION', 'Ficção'),
    ('DOCUMENTARY', 'Documentário'),
    ('ACTION', 'Ação'),
]

class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=12, unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True, unique=True)
    birth_date = models.DateField(null=True, blank=True)

    #pode acessar tela admin do django ou não
    is_staff = models.BooleanField(default=False)
    #se o usuário está ativo ou não
    is_active = models.BooleanField(default=True)

    #login por email:
    USERNAME_FIELD = "email"

    #o que é obrigatório além do padrão (username, email, password)
    REQUIRED_FIELDS = ["cpf"]

    objects = CustomUserManager()


    def __str__(self):
        return self.email
    

class Director(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=1000)
    category = models.CharField(max_length=100,choices=CATEGORIES)
    published_date = models.DateField()
    photo = models.TextField()
    classification = models.IntegerField()
    directors = models.ManyToManyField(Director, null=False)

    def __str__(self):
        return self.title

class Plan(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    
    def __str__(self):
        return self.name

class UserPlan(models.Model):
    plan_FK = models.ForeignKey(Plan, related_name='UserPlan_plan_FK', on_delete=models.CASCADE)
    user_FK = models.ForeignKey(CustomUser, related_name='UserPlan_user_FK', on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user_FK.name}-{self.plan_FK.name}'                

class FavoriteMovie(models.Model):
    movie_FK = models.ForeignKey(Movie, related_name='FavoriteMovie_movie_FK', on_delete=models.CASCADE)
    user_FK = models.ForeignKey(CustomUser, related_name='FavoriteMovie_user_FK', on_delete=models.CASCADE)
   
    def __str__(self):
        return f'{self.user_FK.name}-{self.movie_FK.title}'