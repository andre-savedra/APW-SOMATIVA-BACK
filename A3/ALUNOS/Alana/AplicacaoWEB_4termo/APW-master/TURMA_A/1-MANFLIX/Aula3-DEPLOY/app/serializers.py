from rest_framework import serializers
from .models import *

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
       model = Director
       fields = '__all__'
       many = True

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
       model = Movie
       fields = '__all__'
       many = True

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
       model = Plan
       fields = '__all__'
       many = True

class UserPlanSerializer(serializers.ModelSerializer):
    class Meta:
       model = UserPlan
       fields = '__all__'
       many = True

class FavoriteMovieSerializer(serializers.ModelSerializer):
    class Meta:
       model = FavoriteMovie
       fields = '__all__'
       many = True
