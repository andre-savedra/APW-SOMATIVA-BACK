from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

class AdminCustomUser(UserAdmin):
    model = CustomUser
    list_display = ['id', 'email', 'nif']
    list_display_links = ('id', 'email', 'nif',)

    readonly_fields = ('creation_date',)
    
    fieldsets = (
        (None, {'fields': ('email','password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 
                                    'is_superuser', 'groups', 
                                    'user_permissions',)}),
        ('User data', {'fields': ('nif', 'phone','creation_date',)}),
    )
    filter_horizontal = ('groups', 'user_permissions',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','name','nif','password1','password2'),
        }),
    )
    ordering = ['email']

admin.site.register(CustomUser, AdminCustomUser)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Machine)
admin.site.register(MachineMaintenance)
admin.site.register(Lot)
admin.site.register(Item)