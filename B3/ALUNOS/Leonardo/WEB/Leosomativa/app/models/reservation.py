from django.db import models
from django.utils import timezone
from .accommodation import Accommodation
from .guest import Guest

class Reservation(models.Model):
    # Código identificador da reserva
    code = models.CharField(max_length=10, unique=True)

    # Datas
    check_in = models.DateField()
    check_out = models.DateField()

    # Valor total da reserva
    total_value = models.DecimalField(max_digits=10, decimal_places=2)

    # Status da reserva
    STATUS_CHOICES = [
        ('active', 'Ativa'),
        ('finished', 'Finalizada'),
        ('canceled', 'Cancelada'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    # Relações
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='reservations')
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='reservations')

    # Data de criação automática
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Reserva {self.code} - {self.guest.name}"

    class Meta:
        ordering = ['-check_in']
