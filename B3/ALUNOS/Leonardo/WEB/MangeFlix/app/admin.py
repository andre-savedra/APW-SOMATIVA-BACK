from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import * #após montar a tabela no Models é necessário acrescentar aqui para migrar para o site

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['id','email', 'cpf']
    search_fields = ['email', 'cpf',]
    ordering = ['email']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Director)
admin.site.register(Movie)
admin.site.register(Plan)
admin.site.register(UserPlan)
admin.site.register(FavoriteMovie)
