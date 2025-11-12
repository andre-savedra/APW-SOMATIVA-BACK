from rest_framework.viewsets import ModelViewSet
from ..models import Employee
from ..serializers.employee import EmployeeSerializer

class EmployeeView(ModelViewSet):    
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
