from django.db import models
from .accommodation import Accommodation
from .employee import Employee


class MaintenanceHistory(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='maintenance_history')
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    status_before = models.CharField(max_length=50)
    status_after = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Manutenção {self.accommodation.number} em {self.date}"
