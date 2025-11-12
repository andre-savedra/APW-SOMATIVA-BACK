from rest_framework import serializers
from ..models import Product
from .category import CategorySerializer

class ProductSerializer(serializers.ModelSerializer):
    category_FK = CategorySerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'code', 'category_FK']
        many= True