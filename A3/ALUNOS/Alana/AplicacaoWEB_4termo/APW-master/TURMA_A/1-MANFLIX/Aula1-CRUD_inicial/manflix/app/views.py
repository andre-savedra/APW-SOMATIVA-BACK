from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet

class DirectorsView(ModelViewSet):
    #select * from directors;
    queryset = Directors.objects.all()
    serializer_class = DirectorsSerializer

class MoviesView(ModelViewSet):
    queryset = Movies.objects.all()
    serializer_class = MoviesSerializer

class PlansView(ModelViewSet):
    queryset = Plans.objects.all()
    serializer_class = PlansSerializer

