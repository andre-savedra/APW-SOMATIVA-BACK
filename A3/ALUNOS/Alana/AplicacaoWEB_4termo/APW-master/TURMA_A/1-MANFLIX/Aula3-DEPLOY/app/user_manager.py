from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, cpf=None, **extra_fields):
        #se faltar algum campo, gera erro
        if None in (email,password,cpf):
            raise ValueError("Campo email, senha ou cpf não informados!")
        
        email_ok = self.normalize_email(email)
        
        extra_fields.setdefault("is_active", True)
        #prepara para salvar no banco (construção do objeto)
        user = self.model(email=email_ok, cpf=cpf, **extra_fields)
        #seta a senha e criptografa
        user.set_password(password)
        #salva no banco
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, password=None, cpf=None, **extra_fields):
        #usuário poderá acessar tela de admin do django
        extra_fields.setdefault("is_staff", True)
        #seta no banco do django a propriedade super user para este usuário
        extra_fields.setdefault("is_superuser", True)
        #chama o método padrão de criação de usuário
        return self.create_user(email,password,cpf,**extra_fields)