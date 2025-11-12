from rest_framework import serializers
from .models import Categoria, Produto, Peca, Avaliacao
from orders.models import ItemPedido
from accounts.models import User

# Categoria
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome']

# Peças do Produto
class PecaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peca
        fields = ['id', 'nome', 'medidas', 'peso']

# Produto (inclui categoria e peças)
class ProdutoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    pecas = PecaSerializer(many=True, read_only=True)

    class Meta:
        model = Produto
        fields = ['id', 'nome', 'descricao', 'preco', 'imagem_url', 'categoria', 'pecas', 'estrelas_media', 'total_avaliacoes']

# Avaliação de Produto
class AvaliacaoSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(read_only=True)  # mostra username
    class Meta:
        model = Avaliacao
        fields = ['id', 'usuario', 'produto', 'item', 'nota', 'comentario', 'criado_em']

    def validate_nota(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("A nota deve ser entre 1 e 5.")
        return value

    def create(self, validated_data):
        avaliacao = Avaliacao.objects.create(**validated_data)
        # Atualiza média e total de avaliações do produto
        produto = avaliacao.produto
        total = produto.avaliacoes.count()
        soma = sum(a.nota for a in produto.avaliacoes.all())
        produto.estrelas_media = round(soma / total, 2)
        produto.total_avaliacoes = total
        produto.save()
        return avaliacao
