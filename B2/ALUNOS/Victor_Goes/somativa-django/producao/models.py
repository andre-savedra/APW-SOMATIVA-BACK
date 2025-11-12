from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.db import models

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O email deve ser informado')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not extra_fields.get('is_staff') or not extra_fields.get('is_superuser'):
            raise ValueError('Superuser precisa ter is_staff=True e is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)



class User(AbstractBaseUser, PermissionsMixin):

    ROLES = [
    ('1','Produção'),
    ('2', 'Manutenção'),
    ('3', 'Chefe de Produção'),
    ('4', 'Inspeção'),
]

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    nif = models.CharField(max_length=20, unique=True)
    cpf = models.CharField(max_length=20, unique=True)
    hiring_date = models.DateField()
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=1, choices=ROLES, default='1')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    objects = UserManager()  

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'nif', 'cpf', 'hiring_date']

    def __str__(self):
        return self.email



class Category(models.Model):
      name = models.CharField(max_length=100, unique=True)
   
      def __str__(self):
         return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    codigo = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Machine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Lote(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    responsible = models.ForeignKey(User, on_delete=models.CASCADE)
    inspect_date = models.DateField(null=True, blank=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new or not self.qr_code:
            self.gerar_qrcode()
    
    def gerar_qrcode(self):
        data = f"lote-{self.id}-{self.name}"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        filename = f'qrcode_lote_{self.id}.png'
        self.qr_code.save(filename, ContentFile(buffer.read()), save=False)
        
        super(Lote, self).save(update_fields=['qr_code'])


    def __str__(self):
        return self.name 
    
class Maintence(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.PROTECT)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    responsible = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f'Maintence of {self.machine.name} starting on {self.start_date}'
    
class StatusDashboard(models.Model):
    date = models.DateField()
    total_produced = models.IntegerField()
    total_defective = models.IntegerField()
    production_leader = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f'Status on {self.date} by {self.production_leader.name}'
