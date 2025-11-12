from django.urls import path
from .views import ProdutoListView, ProdutoDetailView, CategoriaListView

urlpatterns = [
    path('produtos/', ProdutoListView.as_view(), name='produtos-list'),
    path('produtos/<int:pk>/', ProdutoDetailView.as_view(), name='produto-detail'),
    path('categorias/', CategoriaListView.as_view(), name='categorias-list'),
]
