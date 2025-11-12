from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet

#Criando API's
class DirectorsView(ModelViewSet):
    queryset = Directors.objects.all() #select * from directors; ou seja select tudo do banco de dados;
    serializer_class = DirectorsSerializer #quem vai converter = Serializer

class MoviesView(ModelViewSet):
    queryset = Movies.objects.all()
    serializer_class = MoviesSerializer

class PlansView(ModelViewSet):
    queryset = Plans.objects.all()
    serializer_class = PlansSerializer

class FavoriteMoviesView(ModelViewSet):
    queryset = FavoriteMovies.objects.all()
    serializer_class = FavoriteMoviesSerializer