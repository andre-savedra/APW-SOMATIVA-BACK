from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, DjangoObjectPermissions, IsAuthenticated
from .models import *
from .serializers import *
from rest_framework.response import Response
from random import randint
from datetime import date
from decimal import *
from .utils import is_Premium

PREMIUM_GAIN_POINTS = 8
BASIC_GAIN_POINTS = 5
LOSS_POINTS = 0.25


class CustomUserView(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
class TokenView(ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    permission_classes = [
        DjangoObjectPermissions
    ]

class AccountView(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    # CUSTOMIZAR

class AccountTokenView(ModelViewSet):
    queryset = AccountToken.objects.all()
    serializer_class = AccountTokenSerializer
    permission_classes = [
        IsAuthenticated
    ]

class BetsView(ModelViewSet):
    queryset = Bets.objects.all()
    serializer_class = BetsSerializer
    permission_classes = [
        IsAuthenticated
    ]

class TransactionsView(ModelViewSet):
    queryset = Transactions.objects.all()
    serializer_class = TransactionsSerializer
    permission_classes = [
        IsAuthenticated
    ]


class BetTryView(APIView):    
    def get(self, request):

        #1 - checa se o usuário não está autenticado:
        if(not request.user.is_authenticated):
            return Response(status=403, data='Você não está autenticado!')
        
        #2 - checa se o usuário é maior de 18 anos:
        birth = request.user.birth_date
        today = date.today()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

        # print(f'DATA NASCIMENTO: {birth}')
        # print(f'SUA IDADE: {age}')
        if (age < 18):
            return Response(status=403, data='Menores de 18 anos não podem realizar jogadas.')


        #3 - checa se o usuário tem saldo positivo de MANGECOIN
        #select *from accounts where user_FK = request.user.id and closing_date = null       
        account = Account.objects.get(user_FK=request.user,closing_date__isnull=True)
        print(f'CONTA ENCONTRADA: {account.id}')

        mangecoins = None
        try:
            #select *from AccountToken where account_FK = account.id and token_FK_id=1
            mangecoins = AccountToken.objects.get(account_FK=account,token_FK_id=1)
            print(f'CONTA DE MANGECOIN: {mangecoins.balance}')
            if mangecoins.balance < LOSS_POINTS:
                return Response(status=403, data=f'Quantidade de MangeCoins insuficiente! SALDO: {mangecoins.balance}')    
        except AccountToken.DoesNotExist:
            return Response(status=403, data='Você não tem nenhuma quantidade de MangeCoins!')

        value1 = randint(0,4)
        value2 = randint(0,4)
        value3 = randint(0,4)

        initial_balance = mangecoins.balance

        #4-adiciona ou retira saldo dependendo do resultado da jogada:
        if value1 == value2 and value2 == value3:
            mangecoins.balance = (mangecoins.balance + 
                                  Decimal(PREMIUM_GAIN_POINTS if is_Premium(request.user.id) else BASIC_GAIN_POINTS))
            #update AccountToken set balance = (balance + 5.0) where id = ?
        else:
           #update AccountToken set balance = (balance - 1.0) where id = ?
           mangecoins.balance = (mangecoins.balance - Decimal(LOSS_POINTS))

        mangecoins.save()

        new_bet = Bets()
        new_bet.account_FK = account
        new_bet.is_loss = bool(initial_balance > mangecoins.balance)
        new_bet.input_amount = initial_balance
        new_bet.output_amount = mangecoins.balance
        new_bet.value1 = value1
        new_bet.value2 = value2
        new_bet.value3 = value3

        # new_bet = Bets(
        #     account_FK=account,
        #     is_loss=bool(initial_balance < mangecoins.balance),
        #     input_amount=initial_balance,
        #     output_amount=mangecoins.balance,
        #     value1=value1,
        #     value2=value2,
        #     value3=value3
        # )
        
        #insert into Bets values (....)
        new_bet.save()

        return Response(status=200, data={
            'bet1': value1,
            'bet2': value2,
            'bet3': value3,
            'new_balance': mangecoins.balance,
        })
