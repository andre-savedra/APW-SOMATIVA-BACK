from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Categoria, Marca, Setor, Produto, Escaninho

class CategoriaSerializer(serializers.ModelSerializer):
    produtos_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'data_registro', 'produtos_count']
        read_only_fields = ['data_registro']
    
    def get_produtos_count(self, obj):
        return obj.produtos.count()

class MarcaSerializer(serializers.ModelSerializer):
    produtos_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Marca
        fields = ['id', 'nome', 'cnpj', 'data_inclusao', 'produtos_count']
        read_only_fields = ['data_inclusao']
    
    def get_produtos_count(self, obj):
        return obj.produtos.count()
    
    def validate_cnpj(self, value):
        # Remove caracteres especiais para validação
        cnpj_numbers = ''.join(filter(str.isdigit, value))
        
        if len(cnpj_numbers) != 14:
            raise serializers.ValidationError("CNPJ deve ter 14 dígitos")
        
        # Formatação automática
        formatted_cnpj = f"{cnpj_numbers[:2]}.{cnpj_numbers[2:5]}.{cnpj_numbers[5:8]}/{cnpj_numbers[8:12]}-{cnpj_numbers[12:14]}"
        return formatted_cnpj

class SetorSerializer(serializers.ModelSerializer):
    escaninhos = serializers.SerializerMethodField()
    escaninhos_count = serializers.SerializerMethodField()
    produtos_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Setor
        fields = ['id', 'nome', 'descricao', 'data_criacao', 'escaninhos', 'escaninhos_count', 'produtos_count']
        read_only_fields = ['data_criacao']
    
    def get_escaninhos(self, obj):
        escaninhos = obj.escaninhos.all()
        return EscaninhoDetailSerializer(escaninhos, many=True).data
    
    def get_escaninhos_count(self, obj):
        return obj.escaninhos.count()
    
    def get_produtos_count(self, obj):
        return obj.escaninhos.filter(produto__isnull=False).count()

class SetorSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setor
        fields = ['id', 'nome', 'descricao']

class ProdutoListSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    marca = MarcaSerializer(read_only=True)
    margem_lucro = serializers.ReadOnlyField()
    dias_cadastrado = serializers.SerializerMethodField()
    
    class Meta:
        model = Produto
        fields = [
            'id', 'nome', 'codigo_registro', 'codigo_barras', 
            'categoria', 'marca', 'data_cadastro', 'custo', 
            'valor_venda', 'informacoes_adicionais', 'em_promocao',
            'margem_lucro', 'dias_cadastrado'
        ]
    
    def get_dias_cadastrado(self, obj):
        delta = timezone.now() - obj.data_cadastro
        return delta.days

class ProdutoCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = [
            'nome', 'codigo_registro', 'codigo_barras', 
            'categoria', 'marca', 'custo', 'valor_venda', 
            'informacoes_adicionais'
        ]
    
    def validate_codigo_barras(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Código de barras deve conter apenas números")
        if len(value) < 8 or len(value) > 13:
            raise serializers.ValidationError("Código de barras deve ter entre 8 e 13 dígitos")
        return value
    
    def validate(self, data):
        if data['valor_venda'] <= data['custo']:
            raise serializers.ValidationError({
                'valor_venda': 'Valor de venda deve ser maior que o custo'
            })
        return data
    
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['criado_por'] = user
        return super().create(validated_data)

class ProdutoPromocaoSerializer(serializers.ModelSerializer):
    """Serializer específico para alterar status de promoção"""
    class Meta:
        model = Produto
        fields = ['em_promocao']
    
    def update(self, instance, validated_data):
        user = self.context['request'].user
        if 'em_promocao' in validated_data:
            instance.promocao_alterada_por = user
            instance.data_promocao = timezone.now()
        return super().update(instance, validated_data)

class EscaninhoDetailSerializer(serializers.ModelSerializer):
    produto = ProdutoListSerializer(read_only=True)
    setor = SetorSimpleSerializer(read_only=True)
    valor_total_estoque = serializers.SerializerMethodField()
    
    class Meta:
        model = Escaninho
        fields = [
            'id', 'codigo', 'setor', 'produto', 'quantidade', 
            'data_criacao', 'data_atualizacao', 'valor_total_estoque'
        ]
    
    def get_valor_total_estoque(self, obj):
        if obj.produto and obj.quantidade > 0:
            return float(obj.produto.valor_venda * obj.quantidade)
        return 0.0

class EscaninhoCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escaninho
        fields = ['codigo', 'setor', 'produto', 'quantidade']
    
    def validate(self, data):
        # Se tem produto, deve ter quantidade > 0
        if data.get('produto') and data.get('quantidade', 0) <= 0:
            raise serializers.ValidationError({
                'quantidade': 'Quantidade deve ser maior que 0 quando há produto'
            })
        
        # Se não tem produto, quantidade deve ser 0
        if not data.get('produto') and data.get('quantidade', 0) > 0:
            raise serializers.ValidationError({
                'quantidade': 'Quantidade deve ser 0 quando não há produto'
            })
        
        return data

class UserSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_admin', 'date_joined']
        read_only_fields = ['date_joined']
    
    def get_is_admin(self, obj):
        return obj.is_staff or obj.is_superuser