from rest_framework import serializers #importando a biblioteca serializers que fica dentro da outra biblioteca rest_framework
from .models import * #importa todos os models

#vamos criar uma serializer para cada model

class DirectorsSerializer(serializers.ModelSerializer):
    class Meta: #classe de configuração
        model = Directors #qual o model, qual tabela do banco de dados
        fields = '__all__' #o que quero converter, nesse caso tudo
        many = True #se pode ter um waei de elementos, nesse caso sim

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

class FavoriteMoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMovies
        fields = '__all__'
        many = True