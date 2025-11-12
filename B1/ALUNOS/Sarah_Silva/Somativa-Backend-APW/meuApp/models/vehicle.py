from django.db import models

Models = [
    ('CAR', 'Carro'),
    ('VAN', 'Van'),
    ('TRUCK', 'Caminhão')
]
class Vehicle(models.Model):
    plate = models.CharField(max_length=8)
    model = models.CharField(max_length=100)
    category = models.CharField(max_length=100,choices=Models)
    acquisition_date = models.DateTimeField()
    last_maintenance = models.DateTimeField()

    def __str__(self):
        return f"{self.category} → {self.plate}"
    