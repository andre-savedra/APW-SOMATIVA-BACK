from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Funcionario, Linha, OrdemProducao, Registro, Alerta, Manutencao

class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = ['id', 'email', 'nome', 'numero_registro', 'cpf', 'data_contratacao', 'cargo']
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """Cria um novo funcionário com senha criptografada."""
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class LinhaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Linha
        fields = ['id', 'nome', 'descricao', 'data_criacao', 'ativa']
        read_only_fields = ['id', 'data_criacao']

class OrdemProducaoSerializer(serializers.ModelSerializer):
    responsavel = FuncionarioSerializer(read_only=True)
    responsavel_id = serializers.PrimaryKeyRelatedField(
        queryset=Funcionario.objects.filter(cargo=Funcionario.Cargo.CHEFE_PRODUCAO),
        write_only=True,
        source='responsavel'
    )
    
    class Meta:
        model = OrdemProducao
        fields = [
            'id', 'numero', 'produto', 'quantidade_planejada', 'quantidade_produzida',
            'linha', 'responsavel', 'responsavel_id', 'data_criacao', 'data_inicio',
            'data_conclusao', 'status', 'observacoes'
        ]
        read_only_fields = ['id', 'data_criacao', 'quantidade_produzida']

class RegistroSerializer(serializers.ModelSerializer):
    funcionario = FuncionarioSerializer(read_only=True)
    funcionario_id = serializers.PrimaryKeyRelatedField(
        queryset=Funcionario.objects.all(),
        write_only=True,
        source='funcionario'
    )

    class Meta:
        model = Registro
        fields = [
            'id', 'ordem_producao', 'funcionario', 'funcionario_id', 'tipo',
            'data_hora', 'quantidade', 'descricao'
        ]
        read_only_fields = ['id', 'data_hora']

class AlertaSerializer(serializers.ModelSerializer):
    criado_por = FuncionarioSerializer(read_only=True)
    criado_por_id = serializers.PrimaryKeyRelatedField(
        queryset=Funcionario.objects.all(),
        write_only=True,
        source='criado_por'
    )
    resolvido_por = FuncionarioSerializer(read_only=True)
    resolvido_por_id = serializers.PrimaryKeyRelatedField(
        queryset=Funcionario.objects.all(),
        write_only=True,
        source='resolvido_por',
        required=False,
        allow_null=True
    )

    class Meta:
        model = Alerta
        fields = [
            'id', 'titulo', 'descricao', 'linha', 'criado_por', 'criado_por_id',
            'data_criacao', 'prioridade', 'resolvido', 'data_resolucao',
            'resolvido_por', 'resolvido_por_id', 'observacoes_resolucao'
        ]
        read_only_fields = ['id', 'data_criacao']

class ManutencaoSerializer(serializers.ModelSerializer):
    responsavel = FuncionarioSerializer(read_only=True)
    responsavel_id = serializers.PrimaryKeyRelatedField(
        queryset=Funcionario.objects.filter(cargo=Funcionario.Cargo.MANUTENCAO),
        write_only=True,
        source='responsavel'
    )

    class Meta:
        model = Manutencao
        fields = [
            'id', 'linha', 'tipo', 'descricao', 'data_agendada', 'responsavel',
            'responsavel_id', 'status', 'data_inicio', 'data_conclusao',
            'observacoes', 'duracao_estimada', 'custo_estimado'
        ]
        read_only_fields = ['id']


from .models import Produto, Maquina, ManutencaoMaquina, Lote, ItemProducao


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'codigo', 'descricao', 'categoria']
        read_only_fields = ['id']


class MaquinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maquina
        fields = ['id', 'codigo', 'foto', 'nome', 'descricao', 'data_criacao']
        read_only_fields = ['id', 'data_criacao']


class ManutencaoMaquinaSerializer(serializers.ModelSerializer):
    responsavel = FuncionarioSerializer(read_only=True)
    responsavel_id = serializers.PrimaryKeyRelatedField(
        queryset=Funcionario.objects.filter(cargo=Funcionario.Cargo.MANUTENCAO),
        write_only=True,
        source='responsavel'
    )

    class Meta:
        model = ManutencaoMaquina
        fields = ['id', 'maquina', 'data_hora', 'descricao', 'responsavel', 'responsavel_id']
        read_only_fields = ['id', 'data_hora']


class LoteSerializer(serializers.ModelSerializer):
    produto = ProdutoSerializer(read_only=True)
    produto_id = serializers.PrimaryKeyRelatedField(queryset=Produto.objects.all(), write_only=True, source='produto')
    responsavel_inspecao = FuncionarioSerializer(read_only=True)
    responsavel_inspecao_id = serializers.PrimaryKeyRelatedField(
        queryset=Funcionario.objects.filter(cargo=Funcionario.Cargo.INSPECAO),
        write_only=True,
        source='responsavel_inspecao',
        required=False,
        allow_null=True
    )

    qr_code = serializers.ImageField(read_only=True)

    class Meta:
        model = Lote
        fields = [
            'id', 'codigo', 'produto', 'produto_id', 'data_hora_inicio', 'data_hora_final',
            'data_inspecao', 'responsavel_inspecao', 'responsavel_inspecao_id', 'status_inspecao',
            'qr_code', 'observacoes'
        ]
        read_only_fields = ['id', 'qr_code']


class ItemProducaoSerializer(serializers.ModelSerializer):
    produto = ProdutoSerializer(read_only=True)
    produto_id = serializers.PrimaryKeyRelatedField(queryset=Produto.objects.all(), write_only=True, source='produto')
    maquina = MaquinaSerializer(read_only=True)
    maquina_id = serializers.PrimaryKeyRelatedField(queryset=Maquina.objects.all(), write_only=True, source='maquina')
    lote = LoteSerializer(read_only=True)
    lote_id = serializers.PrimaryKeyRelatedField(queryset=Lote.objects.all(), write_only=True, source='lote')

    class Meta:
        model = ItemProducao
        fields = ['id', 'lote', 'lote_id', 'produto', 'produto_id', 'data_hora', 'maquina', 'maquina_id', 'identificador']
        read_only_fields = ['id', 'data_hora']