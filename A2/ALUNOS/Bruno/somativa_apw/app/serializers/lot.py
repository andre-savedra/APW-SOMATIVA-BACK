from rest_framework import serializers
from ..models import Lot
from ..serializers.custom_user import CustomUserSerializer
from ..serializers.product import ProductSerializer

class LotSerializer(serializers.ModelSerializer):

    inspector_FK = CustomUserSerializer(read_only=True)
    product_FK = ProductSerializer(read_only=True)

    class Meta:
        model = Lot
        fields = '__all__'
        many= True