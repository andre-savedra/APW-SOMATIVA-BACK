from django.contrib import admin
from .models import Guest, Accommodation, Reservation, Employee, CleaningRecord, MaintenanceRecord

admin.site.register(Guest)
admin.site.register(Accommodation)
admin.site.register(Reservation)
admin.site.register(Employee)
admin.site.register(CleaningRecord)
admin.site.register(MaintenanceRecord)
