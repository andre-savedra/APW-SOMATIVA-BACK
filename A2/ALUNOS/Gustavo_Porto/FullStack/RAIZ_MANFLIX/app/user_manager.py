from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, cpf=None, **extra_fields):
        if None in (email,password,cpf):
            raise ValueError("Campo email, senha ou cpf não informado!")
        email_normalized = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email_normalized, cpf=cpf, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None, cpf=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, cpf, **extra_fields)