from rest_framework import serializers
from ..models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    role = serializers.CharField() 

    class Meta:
        model = Employee
        fields = '__all__'

    def to_representation(self, instance):
        """Transforma o valor técnico em valor legível na saída JSON."""
        data = super().to_representation(instance)
        data['role'] = instance.get_role_display()
        return data
