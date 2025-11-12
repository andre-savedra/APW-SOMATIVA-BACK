from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .custom_user_manager import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    cpf = models.CharField(max_length=12, unique=True)
    rg = models.CharField(max_length=12, unique=True)
    birth_date = models.DateField()
    address_country = models.CharField(max_length=150)
    address_state = models.CharField(max_length=150)
    address_city = models.CharField(max_length=150)
    address_district = models.CharField(max_length=150)
    address_street = models.CharField(max_length=150)
    address_zip_code = models.CharField(max_length=15)
    address_number = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    photo = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'cpf', 'rg', 'birth_date', 
                       'address_country', 'address_state', 'address_city',
                       'address_district', 'address_street', 'address_zip_code',
                       'address_number']
    

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Token(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    token_creation_date = models.DateField()
    insertion_date = models.DateTimeField(auto_now_add=True)
    conversion_rate = models.DecimalField(max_digits=15, decimal_places=4)

    def __str__(self):
        return self.code
    

class Account(models.Model):
    user_FK = models.ForeignKey(CustomUser, related_name='account_user_FK', on_delete=models.CASCADE)
    opening_date = models.DateTimeField(auto_now_add=True)  
    closing_date = models.DateTimeField(null=True, blank=True)
   
    def __str__(self):
        return self.user_FK.email
    

class AccountToken(models.Model):
    account_FK = models.ForeignKey(Account, related_name='accountToken_account_FK', on_delete=models.CASCADE)
    token_FK = models.ForeignKey(Token, related_name='accountToken_token_FK', on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    
    class Meta:
        unique_together = ('account_FK', 'token_FK')

    def __str__(self):
        return f'{self.account_FK.user_FK.email}-{self.token_FK.code}'

class Transaction(models.Model):
    account_FK = models.ForeignKey(Account, related_name='transaction_account_FK', on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True) 
    token_source_FK = models.ForeignKey(Token, related_name='transaction_token_source_FK', on_delete=models.CASCADE)
    token_target_FK = models.ForeignKey(Token, related_name='transaction_token_target_FK', on_delete=models.CASCADE)
    token_source_amount = models.DecimalField(max_digits=15, decimal_places=4)
    token_target_amount = models.DecimalField(max_digits=15, decimal_places=4)
    
    def __str__(self):
        return f'{self.account_FK.user_FK.email}-{self.token_source_FK.code}'


class Bet(models.Model):
    account_FK = models.ForeignKey(Account, related_name='bet_account_FK', on_delete=models.CASCADE)
    is_loss = models.BooleanField(default=True)
    input_amount = models.DecimalField(max_digits=15, decimal_places=2)
    output_amount = models.DecimalField(max_digits=15, decimal_places=2)
    value1 = models.IntegerField()
    value2 = models.IntegerField()
    value3 = models.IntegerField()
    bet_date = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.account_FK.user_FK.email
