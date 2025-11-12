from django.contrib import admin
from .models import Categoria, Marca, Setor, Escaninho, Produto

# registra models pra aparecerem na pag de admin:
admin.site.register(Categoria)
admin.site.register(Marca)
admin.site.register(Setor)
admin.site.register(Escaninho)
admin.site.register(Produto)