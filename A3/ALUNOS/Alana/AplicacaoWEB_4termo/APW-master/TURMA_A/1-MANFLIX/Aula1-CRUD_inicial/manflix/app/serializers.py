from rest_framework import serializers
from .models import *

class DirectorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Directors
        fields = '__all__'
        many = True

class MoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = '__all__'
        many = True

class PlansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plans
        fields = '__all__'
        many = True