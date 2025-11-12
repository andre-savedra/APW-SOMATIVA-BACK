from django.db import models

class Machine(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    photo = models.ImageField(null=True)

    def __str__(self):
        return self.name
    
class MachineMaintenance(models.Model):
    date = models.DateTimeField(null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    machine_FK = models.ForeignKey('Machine', 
                                related_name='MachineMaintenance_machine_FK',
                                on_delete=models.CASCADE)
    user_FK = models.ForeignKey('CustomUser', 
                                related_name='MachineMaintenance_user_FK',
                                on_delete=models.SET_NULL,
                                null=True)
    
    def __str__(self):
        return f"Manutenção da máquina {self.machine_FK}"