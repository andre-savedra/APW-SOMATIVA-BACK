from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Product, Machine, Lote, Maintence, StatusDashboard

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'nif', 'cpf', 'hiring_date', 'role', 'is_staff', 'is_active', 'password']
        # Adicionei 'role' aqui ↑

    def create(self, validated_data):
        pwd = validated_data.pop('password', None)
        user = User(**validated_data)
        if pwd:
            user.set_password(pwd)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        pwd = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if pwd:
            instance.set_password(pwd)
        instance.save()
        return instance

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(write_only=True, source='category', queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = '__all__'

class MaintenceSerializer(serializers.ModelSerializer):
    responsible = UserSerializer(read_only=True)
    responsible_id = serializers.PrimaryKeyRelatedField(write_only=True, source='responsible', queryset=User.objects.all())

    class Meta:
        model = Maintence
        fields = '__all__'

class MachineSerializer(serializers.ModelSerializer):
    maintenances = MaintenceSerializer(many=True, read_only=True, source='maintence_set')

    class Meta:
        model = Machine
        fields = '__all__'

class LoteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(write_only=True, source='product', queryset=Product.objects.all())
    responsible = UserSerializer(read_only=True)
    responsible_id = serializers.PrimaryKeyRelatedField(write_only=True, source='responsible', queryset=User.objects.all())

    class Meta:
        model = Lote
        fields = '__all__'

class DashboardLoteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    responsible = UserSerializer(read_only=True)
    inspector = UserSerializer(read_only=True)
    machine = MachineSerializer(read_only=True)
    maintenances = MaintenceSerializer(many=True, read_only=True)

    class Meta:
        model = Lote
        fields = '__all__'
        depth = 2

class DashboardStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusDashboard
        fields = '__all__'
        depth = 2