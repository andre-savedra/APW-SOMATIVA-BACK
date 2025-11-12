from django.db import models
from django.utils import timezone

EmployeeRole = [
    ('DRIVER', 'Motorista'),
    ('MECHANIC', 'Mecânico'),
    ('FLEET_SUPERVISOR', 'Supervisor da Frota'),
    ('ENGINEER', 'Engenheiro'),
    ('ADMIN', 'Administrador'),
]


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=14, unique=True) 
    hire_date = models.DateField(default=timezone.now)
    role = models.CharField(max_length=20, choices=EmployeeRole)

    def __str__(self):
        return f"{self.name} ({self.role})"
