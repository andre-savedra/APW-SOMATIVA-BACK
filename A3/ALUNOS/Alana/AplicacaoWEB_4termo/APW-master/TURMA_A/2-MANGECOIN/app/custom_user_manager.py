from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password, cpf, rg, birth_date,
                       address_street, address_district, address_number,
                       address_zip_code, address_city, address_state, 
                       address_country, phone, **extra_fields):
        
        if None in (name, email, password, cpf, rg, birth_date,
                    address_street, address_district, address_number,
                    address_zip_code, address_city, address_state, 
                    address_country, phone):
            raise ValueError('Missing required fields!')
        
        extra_fields.setdefault('is_active', True)
        user = self.model(email=self.normalize_email(email), 
                          name=name, cpf=cpf, rg=rg, birth_date=birth_date,
                          address_street=address_street, address_district=address_district,
                          address_number=address_number, address_zip_code=address_zip_code,
                          address_city=address_city, address_state=address_state,
                          address_country=address_country, phone=phone, 
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, name, email, password, cpf, rg, birth_date,
                       address_street, address_district, address_number,
                       address_zip_code, address_city, address_state, 
                       address_country, phone, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(name, email, password, cpf, rg, birth_date,
                       address_street, address_district, address_number,
                       address_zip_code, address_city, address_state, 
                       address_country, phone, **extra_fields)