from rest_framework import serializers
from ..models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    guest_name = serializers.CharField(source='guest.user.get_full_name', read_only=True)
    accommodation_number = serializers.CharField(source='accommodation.number', read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'code', 'guest', 'guest_name', 'accommodation', 'accommodation_number',
                  'check_in', 'check_out', 'total_value', 'status']
