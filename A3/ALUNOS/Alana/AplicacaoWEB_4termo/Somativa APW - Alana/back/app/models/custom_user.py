from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class CustomUserManager(BaseUserManager):
    # Criar usuário comum
    def create_user(self, email, password=None, name=None, **extra_fields):
        if not email:
            raise ValueError("O email é obrigatório!")
        if not name:
            raise ValueError("O nome é obrigatório!")

        email = self.normalize_email(email)

        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Criar um superusuário (admin)
    def create_superuser(self, email, password, name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email=email, password=password, name=name, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    
    # Permissões
    is_staff = models.BooleanField(default=False)  # Pode acessar o admin
    is_active = models.BooleanField(default=True)
    
    creation_date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
