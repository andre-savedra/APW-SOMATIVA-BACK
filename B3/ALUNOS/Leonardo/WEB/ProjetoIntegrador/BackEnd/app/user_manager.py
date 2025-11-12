from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, registro, password=None, cpf=None, email=None, **extra_fields):
        if None in (registro, password, cpf):
            raise ValueError("Campos 'registro', 'senha' ou 'cpf' não informados!")

        if email:
            email = self.normalize_email(email)

        extra_fields.setdefault("is_active", True)

        user = self.model(
            registro=registro,
            cpf=cpf,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, registro, password=None, cpf=None, email=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(registro, password=password, cpf=cpf, email=email, **extra_fields)
