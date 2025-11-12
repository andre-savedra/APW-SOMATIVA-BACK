
from rest_framework import serializers
from app.models.accommodation import Accommodation  

class AccommodationSerializer(serializers.ModelSerializer):
    last_cleaning_employee_name = serializers.CharField(
        source='last_cleaning_employee.user.get_full_name',  
        read_only=True
    )

    class Meta:
        model = Accommodation
        fields = [
            'id', 'number', 'type', 'max_guests', 'daily_rate', 'status',
            'last_cleaning_date', 'last_cleaning_employee_name'
        ]
