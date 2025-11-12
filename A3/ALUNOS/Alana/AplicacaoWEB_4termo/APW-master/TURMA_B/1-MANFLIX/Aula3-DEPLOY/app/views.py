from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet

class DirectorView(ModelViewSet):    
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

class MovieView(ModelViewSet):    
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class PlanView(ModelViewSet):    
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

class UserPlanView(ModelViewSet):    
    queryset = UserPlan.objects.all()
    serializer_class = UserPlanSerializer

class FavoriteMovieView(ModelViewSet):    
    queryset = FavoriteMovie.objects.all()
    serializer_class = FavoriteMovieSerializer