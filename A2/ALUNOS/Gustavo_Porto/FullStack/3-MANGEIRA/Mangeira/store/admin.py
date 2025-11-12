from django.contrib import admin
from .models import Categoria, Produto, Peca, Avaliacao

# Categoria
admin.site.register(Categoria)

# Produto
admin.site.register(Produto)

# Peças
admin.site.register(Peca)

# Avaliações
admin.site.register(Avaliacao)
