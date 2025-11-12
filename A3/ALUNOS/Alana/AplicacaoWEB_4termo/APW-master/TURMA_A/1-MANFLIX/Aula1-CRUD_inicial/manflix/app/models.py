from django.db import models


CATEGORIES = [
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
   directors = models.ManyToManyField(Directors)
   classification = models.IntegerField()

   def __str__(self):
      return self.title

class Plans(models.Model):
   name = models.CharField(max_length=200,null=False,blank=False)
   price = models.DecimalField(max_digits=6,decimal_places=2)

   def __str__(self):
      return self.name

  
