from rest_framework import serializers
from ..models import *

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['nome','email',' cpf','Cargo','id']
        many= True

