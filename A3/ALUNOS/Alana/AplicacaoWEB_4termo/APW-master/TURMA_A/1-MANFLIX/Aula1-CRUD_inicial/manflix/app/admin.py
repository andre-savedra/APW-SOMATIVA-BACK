from django.contrib import admin
from .models import *

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title','category', 'classification')
    search_fields = ('title','category',)

admin.site.register(Directors)
admin.site.register(Movies,MovieAdmin)
admin.site.register(Plans)

