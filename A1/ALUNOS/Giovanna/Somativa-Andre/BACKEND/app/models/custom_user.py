from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin


class CustomUserManeger(BaseUserManager):

    def create_user(self,email, cpf,password, **extra_fields ):
       if None in (email,password,cpf):
           raise ValueError("Email,password ou CPF Invalidos !")
       
       extra_fields.setdefault('is_active',True)
       user = self.model(email=self.normalize_email(email),cpf=cpf,
                         **extra_fields)
       
       user.set_password(password)
       user.save(using=self._db)
       return user
    

    def create_superuser(self,email, cpf,password, **extra_fields):
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(email,cpf,password,**extra_fields)
    
class Cargo(models.TextChoices):
    Produção =  'Produção'
    LIDER_PRODUÇÃO = 'LIDER_PRODUÇÃO'
    INSPEÇÃO= 'INSPEÇÃO'
    ENGENHARIA = ' ENGENHARIA'
    MANUTENÇÃO='MANUTENÇÃO'
    ADMIN= ' ADMIN'


class CustomUser(AbstractBaseUser,PermissionsMixin):
    nome =models.CharField(max_length=150)
    email = models.EmailField(max_length=255, unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    numero_registro= models.CharField(max_length=15)
    data_contrato = models.DateTimeField(auto_now_add=True)
    Cargo = models.CharField(max_length=50, choices=Cargo.choices)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['cpf', 'nome']
    objects = CustomUserManeger()

    def __str__(self):
        return self.email