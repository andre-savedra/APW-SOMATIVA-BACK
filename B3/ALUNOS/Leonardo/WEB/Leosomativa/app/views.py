# app/views.py
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Accommodation
from .serializers import AccommodationSerializer

@api_view(['GET'])
def accommodations_not_cleaned(request):
    seven_days_ago = timezone.now().date() - timedelta(days=7)
    queryset = Accommodation.objects.filter(last_cleaning_date__lte=seven_days_ago)
    serializer = AccommodationSerializer(queryset, many=True)
    return Response(serializer.data)
