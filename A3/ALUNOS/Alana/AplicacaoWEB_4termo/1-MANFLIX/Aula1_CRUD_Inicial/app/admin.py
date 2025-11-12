from django.contrib import admin

from .models import *

admin.site.register(Movie)
admin.site.register(Director)
admin.site.register(Plan)
admin.site.register(UserPlan)
admin.site.register(FavoriteMovie)