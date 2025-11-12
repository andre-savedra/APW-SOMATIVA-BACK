from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from .vehicle import Vehicle
from .employee import Employee, EmployeeRole

MaintenanceType = [
    ('PREVENTIVE', 'Preventivo'),
    ('CORRECTIVE', 'Corretivo')
]
class Maintenance(models.Model):
    code = models.CharField(max_length=20, unique=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenances')
    date = models.DateField(default=timezone.now)
    type = models.CharField(max_length=15, choices=MaintenanceType)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    technician = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        limit_choices_to={'role': 'MECHANIC'},
        related_name='maintenances'
    )

    def __str__(self):
        return f"Maintenance {self.code} - {self.vehicle}"
