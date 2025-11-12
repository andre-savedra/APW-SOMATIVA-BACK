from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Trip
from ..serializers.trip import TripSerializer
from ..filters import TripFilter

class TripView(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    filterset_class = TripFilter
