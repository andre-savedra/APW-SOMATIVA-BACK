#responsavel por fazer o CRUD nas classes
#A API é construída com essa duas linhas queryset e serializer

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .serializers import *
from .models import *
from random import randint #essa biblioteca é para numeros inteiros
from rest_framework.response import Response
from datetime import date
from .utils import isPremium

GAIN_POINTS = 5
GAIN_POINTS_PREMIUM = 8
LOSS_POINTS = 1

#São construídas API´s para todas as tabelas para CRUD dos dados

class CustomUserView(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class AccountView(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class TokenView(ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer

class AccountTokenView(ModelViewSet):
    queryset = AccountToken.objects.all()
    serializer_class = AccountTokenSerializer

class TransactionView(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class BetView(ModelViewSet):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer

#Aqui começa a fazer a lógica para utilização do jogo de roleta

#1 - apenas usuários autenticados podem fazer jogadas
#2 - apenas usuários 18 + podem fazer jogadas
#3 - apenas usuários com saldo positivo em MANGECOIN podem jogar

class BetTryView(APIView):

    def get(self, request):

        #logica para o usuario autenticado poder jogar
        #Foi feito a autenticacao do usuario usando o Djoser
        if not request.user.is_authenticated: #busca se o usuario esta authenticado
            return Response(status=403,data='Usuário não está autenticado!')
        
        #logica para maiores de 18 anos poder jogar
        birth = request.user.birth_date #buscando a data de nascimento
        today = date.today() #criada uma variavel
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day)) #Se o dia de hoje (today) for menor que o aniversario vai dizer que o usuario ainda não tem 18 anos

        print("DATA DE NASCIMENTO DO USUÁRIO: ", birth) #esses prints são para teste no terminal para enxergar a data cadastrada
        print("IDADE DO USUÁRIO: ", age)

        if age < 18:
            return Response(status=403,
                            data='Jogadas permitidas apenas p/ maiores de 18 anos.')

        #logica para buscar o saldo do usuario na tabela Account e autorizar a jogada
        mangecoins = None
        try:
            # select *from Account where user_FK = x and closing_date is null;
            account = Account.objects.get(user_FK=request.user,closing_date__isnull=True)
            mangecoins = AccountToken.objects.get(account_FK=account,token_FK_id=1)
            if (mangecoins.balance < LOSS_POINTS):
                return Response(status=403,
                            data=f'Você não tem saldo suficiente em Mangecoin para fazer uma jogada. SALDO: {mangecoins.balance}')    
        except (AccountToken.DoesNotExist, Account.DoesNotExist):
            return Response(status=403,
                            data='Você não tem registros de Mangecoin. Compre o token para poder jogar.')
        
        #3 roletas de 5 imagens (0,1,2,3,4)
        value1 = randint(0,4) # randint numero randomico inteiro de 0 a 4
        value2 = randint(0,4)
        value3 = randint(0,4)

        #saldo antigo : 3
        old_balance = mangecoins.balance
        #verificar se o usuário ganhou ou perdeu
        if (value1 == value2 and value2 == value3):
            mangecoins.balance = mangecoins.balance + (
                GAIN_POINTS_PREMIUM if isPremium(request.user.id) 
                else GAIN_POINTS)
        else:
            mangecoins.balance = mangecoins.balance - LOSS_POINTS

        mangecoins.save()

        new_bet = Bet(
            account_FK=mangecoins.account_FK,
            is_loss=bool(old_balance > mangecoins.balance),
            input_amount=old_balance,
            output_amount=mangecoins.balance,
            value1=value1,
            value2=value2,
            value3=value3,
        )
        # insert into Bet values (....);
        new_bet.save()

        return Response(status=200,data={
            'bet1': value1,
            'bet2': value2,
            'bet3': value3,
            'new_balance': mangecoins.balance,
        })
