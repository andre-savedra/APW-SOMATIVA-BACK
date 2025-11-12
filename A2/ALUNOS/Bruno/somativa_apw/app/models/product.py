from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    category_FK = models.ForeignKey('Category', 
                                related_name='Product_category_FK',
                                on_delete=models.SET_NULL,
                                null=True)

    def __str__(self):
        return self.name