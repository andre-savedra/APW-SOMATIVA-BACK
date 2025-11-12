from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Reservation
from ..serializers import ReservationSerializer
from ..permissions import ReceptionReservationPermission

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated, ReceptionReservationPermission]
