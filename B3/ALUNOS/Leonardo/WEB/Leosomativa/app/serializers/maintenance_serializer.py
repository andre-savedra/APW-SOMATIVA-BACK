# serializers/maintenance_serializer.py
from rest_framework import serializers
from ..models import MaintenanceHistory
from ..serializers import AccommodationSerializer
from ..serializers import EmployeeSerializer

class MaintenanceHistorySerializer(serializers.ModelSerializer):
    accommodation = AccommodationSerializer(read_only=True)
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = MaintenanceHistory
        fields = ['id', 'accommodation', 'employee', 'status_before', 'status_after', 'description', 'date']
