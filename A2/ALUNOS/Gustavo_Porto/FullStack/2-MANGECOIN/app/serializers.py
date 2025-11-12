from .models import *
from rest_framework import serializers

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        many = True

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        many = True

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'
        many = True

class AccountTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountToken
        fields = '__all__'
        many = True

class BetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bets
        fields = '__all__'
        many = True

class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'
        many = True
