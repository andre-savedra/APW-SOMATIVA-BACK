
from rest_framework import serializers
from .models import User, Produto, Lote, Maquina, Manutencao, ItemProduzido

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'cpf', 'data_contratacao', 'numero_registro', 'first_name', 'last_name']

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

class ItemProduzidoSerializer(serializers.ModelSerializer):
    maquina_nome = serializers.CharField(source='maquina.nome', read_only=True)
    
    class Meta:
        model = ItemProduzido
        fields = ['id', 'data_hora', 'maquina', 'maquina_nome']

class LoteSerializer(serializers.ModelSerializer):
    responsavel_inspecao_nome = serializers.CharField(source='responsavel_inspecao.get_full_name', read_only=True)
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    itens_produzidos = ItemProduzidoSerializer(many=True, read_only=True, source='itens')
    total_itens = serializers.SerializerMethodField()

    class Meta:
        model = Lote
        fields = '__all__'

    def get_total_itens(self, obj):
        return obj.itens.count()

class ManutencaoSerializer(serializers.ModelSerializer):
    funcionario_nome = serializers.CharField(source='funcionario.get_full_name', read_only=True)
    
    class Meta:
        model = Manutencao
        fields = '__all__'

class MaquinaSerializer(serializers.ModelSerializer):
    manutencoes = ManutencaoSerializer(many=True, read_only=True)
    ultima_manutencao = serializers.SerializerMethodField()
    precisa_manutencao = serializers.SerializerMethodField()

    class Meta:
        model = Maquina
        fields = '__all__'

    def get_ultima_manutencao(self, obj):
        ultima = obj.manutencoes.order_by('-data_hora').first()
        if ultima:
            return ManutencaoSerializer(ultima).data
        return None

    def get_precisa_manutencao(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        
        ultima_manutencao = obj.manutencoes.order_by('-data_hora').first()
        if not ultima_manutencao:
            return True
        
        dois_meses_atras = timezone.now() - timedelta(days=60)
        return ultima_manutencao.data_hora < dois_meses_atras

class DashboardSerializer(serializers.Serializer):
    total_aprovadas = serializers.IntegerField()
    total_reprovadas = serializers.IntegerField()
    taxa_aprovacao = serializers.FloatField()
    periodo_inicio = serializers.DateField()
    periodo_fim = serializers.DateField()