from django.db import models
from django.conf import settings

class Employee(models.Model):
    # Vincula o funcionário a um usuário do sistema (Custom User)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='employee_profile'
    )

    registration_number = models.CharField(max_length=20, unique=True)  # matrícula

    # Cargos disponíveis
    POSITION_CHOICES = [
        ('reception', 'Recepção'),
        ('housekeeping', 'Governança'),
        ('maintenance', 'Manutenção'),
        ('management', 'Gerência'),
        ('admin', 'Admin'),
    ]
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)

    hire_date = models.DateField()  # data de contratação

    def __str__(self):
    # Sempre tenta pegar o nome do user
        if self.user and getattr(self.user, 'name', None):
         return self.user.name
        return f'Funcionário {self.pk}'

