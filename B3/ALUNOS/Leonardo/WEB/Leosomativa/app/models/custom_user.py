from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group, Permission

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, name, nif, **extra_fields):
        if None in (email,password,name,nif):
            raise ValueError("Email, Password, Name or Nif are invalid!")
        
        extra_fields.setdefault('is_active', True)
        user = self.model(email=self.normalize_email(email),
                          nif=nif,
                          name=name,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, name, nif, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email,password,name,nif,**extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250, unique=True)
    nif = models.CharField(max_length=15)
    phone = models.CharField(max_length=15, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  
        blank=True,
        help_text='Specific permissions for this user.'
    )

    # Login pelo email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'nif']

    objects = CustomUserManager()

    def __str__(self):
        return self.name
