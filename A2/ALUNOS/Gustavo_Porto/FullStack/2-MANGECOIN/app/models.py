from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .custom_user_manager import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    cpf = models.CharField(max_length=12, unique=True)
    rg = models.CharField(max_length=12, unique=True)
    birth_date = models.DateField()
    address_street = models.CharField(max_length=400)
    address_district = models.CharField(max_length=400)
    address_number = models.CharField(max_length=10)
    address_zip_code = models.CharField(max_length=15)
    address_city = models.CharField(max_length=400)
    address_state = models.CharField(max_length=400)
    address_country = models.CharField(max_length=400)
    phone = models.CharField(max_length=15,unique=True)
    photo = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','cpf','rg','birth_date',
                       'address_street', 'address_district', 'address_number',
                       'address_zip_code', 'address_city', 'address_state', 
                       'address_country','phone']

    objects = CustomUserManager()

    def __str__(self):
        return self.email



class Token(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)    
    token_creation_date = models.DateTimeField()
    insertion_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    conversion_rate = models.DecimalField(max_digits=12, decimal_places=4)

    def __str__(self):
        return self.code

class Account(models.Model):
    user_FK = models.ForeignKey(CustomUser, related_name='Account_user_FK', on_delete=models.CASCADE)    
    opening_date = models.DateTimeField(auto_now_add=True)
    closing_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.user_FK.email

class AccountToken(models.Model):
    account_FK = models.ForeignKey(Account, related_name='AccountToken_account_FK', on_delete=models.CASCADE)    
    token_FK = models.ForeignKey(Token, related_name='AccountToken_token_FK', on_delete=models.CASCADE)    
    balance = models.DecimalField(max_digits=12, decimal_places=4)
    # balance = models.FloatField()
    
    #garante unicidade entre conta + token
    class Meta:
        unique_together = ('account_FK', 'token_FK')
        
    def __str__(self):
        return f'{self.account_FK.id}-{self.token_FK.name}'
    
    
class Transactions(models.Model):
    account_FK = models.ForeignKey(Account, related_name='Transactions_account_FK', on_delete=models.CASCADE)    
    transaction_date = models.DateTimeField(auto_now_add=True)
    token_source_FK = models.ForeignKey(Token, related_name='Transactions_token_source_FK', on_delete=models.CASCADE)    
    token_target_FK = models.ForeignKey(Token, related_name='Transactions_token_target_FK', on_delete=models.CASCADE)    
    token_source_amount = models.DecimalField(max_digits=12, decimal_places=4)
    token_target_amount = models.DecimalField(max_digits=12, decimal_places=4)
        
    def __str__(self):
        return f'{self.token_source_FK.name}-{self.token_target_FK.name}'


class Bets(models.Model):
    account_FK = models.ForeignKey(Account, related_name='Bets_account_FK', on_delete=models.CASCADE)    
    is_loss = models.BooleanField(default=True)
    input_amount = models.DecimalField(max_digits=12, decimal_places=4)
    output_amount = models.DecimalField(max_digits=12, decimal_places=4)
    value1 = models.IntegerField()
    value2 = models.IntegerField()
    value3 = models.IntegerField()

    def __str__(self):
        return self.account_FK.user_FK.name