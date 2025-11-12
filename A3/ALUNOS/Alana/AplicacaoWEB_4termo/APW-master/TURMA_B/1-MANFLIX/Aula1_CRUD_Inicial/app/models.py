from django.db import models
from django.contrib.auth.models import User

CATEGORIES = [
    ('HORROR','Terror'),
    ('COMEDY', 'Comédia'),
    ('FICCTION', 'Ficção'),
    ('DOCUMENTARY', 'Documentário'),
    ('ACTION', 'Ação'),
]

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
    user_FK = models.ForeignKey(User, related_name='UserPlan_user_FK', on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user_FK.username}-{self.plan_FK.name}'                

class FavoriteMovie(models.Model):
    movie_FK = models.ForeignKey(Movie, related_name='FavoriteMovie_movie_FK', on_delete=models.CASCADE)
    user_FK = models.ForeignKey(User, related_name='FavoriteMovie_user_FK', on_delete=models.CASCADE)
   
    def __str__(self):
        return f'{self.user_FK.username}-{self.movie_FK.title}'