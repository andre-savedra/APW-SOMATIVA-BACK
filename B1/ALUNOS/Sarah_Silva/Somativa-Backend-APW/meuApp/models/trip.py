from django.db import models
from django.core.validators import MinValueValidator
from .vehicle import Vehicle
from .employee import Employee, EmployeeRole

class Trip(models.Model):
    code = models.CharField(max_length=20, unique=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='trips')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    destination = models.CharField(max_length=100)
    mileage = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    driver = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        limit_choices_to={'role': 'DRIVER'},
        related_name='trips'
    )

    def __str__(self):
        return f"Trip {self.code} - {self.vehicle.license_plate}"
