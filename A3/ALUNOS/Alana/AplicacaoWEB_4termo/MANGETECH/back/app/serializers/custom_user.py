from rest_framework import serializers
from ..models import *

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'nif', 'phone'] #selecionamos o que queremos exibir de acordo com o que colocamos no models
        many= True