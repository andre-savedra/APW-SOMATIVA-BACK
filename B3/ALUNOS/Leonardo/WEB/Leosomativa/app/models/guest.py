from django.db import models

class Guest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name