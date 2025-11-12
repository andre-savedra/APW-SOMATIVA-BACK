from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Categoria, Marca, Setor, Produto, Escaninho

class CategoriaSerializer(serializers.ModelSerializer):
    total_produtos = serializers.SerializerMethodField()

    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'data_registro', 'total_produtos']

    def get_total_produtos(self, obj):
        return obj.produtos.count()

class MarcaSerializer(serializers.ModelSerializer):
    total_produtos = serializers.SerializerMethodField()

    class Meta:
        model = Marca
        fields = ['id', 'nome', 'cnpj', 'data_inclusao', 'total_produtos']

    def get_total_produtos(self, obj):
        return obj.produtos.count()

# Serializer básico do Produto (sem detalhes para evitar recursão)
class ProdutoBasicoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    marca_nome = serializers.CharField(source='marca.nome', read_only=True)

    class Meta:
        model = Produto
        fields = [
            'id', 'nome', 'codigo_registro', 'codigo_barras',
            'categoria_nome', 'marca_nome', 'custo', 'valor_venda',
            'em_promocao', 'data_cadastro'
        ]

# Serializer básico do Escaninho (sem detalhes para evitar recursão)
class EscaninhoBasicoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    localizacao_completa = serializers.ReadOnlyField()

    class Meta:
        model = Escaninho
        fields = [
            'id', 'codigo', 'produto_nome', 'quantidade',
            'localizacao_completa', 'data_atualizacao'
        ]

class SetorSerializer(serializers.ModelSerializer):
    total_escaninhos = serializers.SerializerMethodField()
    escaninhos = serializers.SerializerMethodField()

    class Meta:
        model = Setor
        fields = ['id', 'letra', 'descricao', 'data_criacao', 'total_escaninhos', 'escaninhos']

    def get_total_escaninhos(self, obj):
        return obj.escaninhos.count()

    def get_escaninhos(self, obj):
        # Só incluir escaninhos na visualização detalhada (detail view)
        request = self.context.get('request')
        if request and hasattr(request, 'resolver_match') and request.resolver_match:
            if hasattr(request.resolver_match, 'url_name') and request.resolver_match.url_name and 'detail' in request.resolver_match.url_name:
                escaninhos = obj.escaninhos.all()
                return EscaninhoBasicoSerializer(escaninhos, many=True).data
        return []

class ProdutoSerializer(serializers.ModelSerializer):
    categoria_detalhes = CategoriaSerializer(source='categoria', read_only=True)
    marca_detalhes = MarcaSerializer(source='marca', read_only=True)
    margem_lucro = serializers.ReadOnlyField()
    localizacoes = serializers.SerializerMethodField()

    class Meta:
        model = Produto
        fields = [
            'id', 'nome', 'codigo_registro', 'codigo_barras',
            'categoria', 'categoria_detalhes', 'marca', 'marca_detalhes',
            'data_cadastro', 'custo', 'valor_venda', 'informacoes_adicionais',
            'em_promocao', 'margem_lucro', 'localizacoes'
        ]

    def get_localizacoes(self, obj):
        escaninhos = obj.escaninhos.filter(quantidade__gt=0)
        return [
            {
                'setor': escaninho.setor.letra,
                'escaninho': escaninho.codigo,
                'quantidade': escaninho.quantidade,
                'localizacao_completa': escaninho.localizacao_completa
            }
            for escaninho in escaninhos
        ]

class EscaninhoSerializer(serializers.ModelSerializer):
    setor_letra = serializers.CharField(source='setor.letra', read_only=True)
    produto_detalhes = ProdutoBasicoSerializer(source='produto', read_only=True)
    esta_vazio = serializers.ReadOnlyField()
    localizacao_completa = serializers.ReadOnlyField()

    class Meta:
        model = Escaninho
        fields = [
            'id', 'codigo', 'setor', 'setor_letra',
            'produto', 'produto_detalhes', 'quantidade',
            'data_criacao', 'data_atualizacao', 'esta_vazio', 'localizacao_completa'
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser']
        read_only_fields = ['id', 'is_staff', 'is_superuser']