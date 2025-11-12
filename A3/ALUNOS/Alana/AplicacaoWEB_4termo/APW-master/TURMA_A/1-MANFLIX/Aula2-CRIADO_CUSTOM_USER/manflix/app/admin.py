from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['id','email','cpf']
    search_fields = ['email','cpf',]
    ordering = ['email']

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title','category', 'classification')
    search_fields = ('title','category',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Directors)
admin.site.register(Movies,MovieAdmin)
admin.site.register(Plans)
admin.site.register(FavoriteMovies)

