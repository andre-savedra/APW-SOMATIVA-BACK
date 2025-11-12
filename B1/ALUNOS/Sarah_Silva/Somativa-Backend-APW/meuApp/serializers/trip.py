from rest_framework import serializers
from ..models import Trip, Employee, Vehicle

class TripSerializer(serializers.ModelSerializer):
    driver = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.filter(role='DRIVER')
    )
    vehicle = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.all()
    )

    class Meta:
        model = Trip
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['driver'] = instance.driver.name  
        data['vehicle'] = instance.vehicle.model  
        return data
