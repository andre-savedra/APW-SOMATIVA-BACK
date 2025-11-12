from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import RegexValidator, MinValueValidator
from django.core.files.base import ContentFile
from io import BytesIO

class FuncionarioManager(BaseUserManager):
    def create_user(self, email, nome, numero_registro, cpf, password=None, **extra_fields):
        if not email:
            raise ValueError(_('O endereço de email é obrigatório'))
        if not nome:
            raise ValueError(_('O nome é obrigatório'))
        if not numero_registro:
            raise ValueError(_('O número de registro é obrigatório'))
        if not cpf:
            raise ValueError(_('O CPF é obrigatório'))
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            nome=nome,
            numero_registro=numero_registro,
            cpf=cpf,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, numero_registro, cpf, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('cargo', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superusuário deve ter is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superusuário deve ter is_superuser=True.'))

        return self.create_user(email, nome, numero_registro, cpf, password, **extra_fields)

class Funcionario(AbstractUser):
    """Modelo customizado de usuário (Funcionário) que substitui o User padrão."""

    class Cargo(models.TextChoices):
        PRODUCAO = 'PRODUCAO', _('Produção')
        CHEFE_PRODUCAO = 'CHEFE_PRODUCAO', _('Chefe de Produção')
        INSPECAO = 'INSPECAO', _('Inspeção')
        MANUTENCAO = 'MANUTENCAO', _('Manutenção')
        ADMIN = 'ADMIN', _('Admin')

    username = None  # Remove o campo username padrão
    email = models.EmailField(_('endereço de email'), unique=True)
    nome = models.CharField(_('nome completo'), max_length=150)
    numero_registro = models.CharField(_('número de registro'), max_length=50, unique=True)
    cpf = models.CharField(
        _('CPF'),
        max_length=11,
        unique=True,
        help_text=_('Digite apenas os 11 números do CPF, sem pontos ou traços'),
        validators=[RegexValidator(r'^\d{11}$', _('CPF deve conter exatamente 11 dígitos numéricos'))]
    )
    data_contratacao = models.DateField(_('data de contratação'), default=timezone.now)
    cargo = models.CharField(
        _('cargo'),
        max_length=20,
        choices=Cargo.choices,
        default=Cargo.PRODUCAO
    )

    # Adicionando related_name para evitar conflitos
    groups = models.ManyToManyField(
        Group,
        related_name="funcionarios_groups",
        verbose_name=_('grupos'),
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="funcionarios_permissions",
        verbose_name=_('permissões de usuário'),
        blank=True
    )

    objects = FuncionarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'numero_registro', 'cpf']

    class Meta:
        verbose_name = _('funcionário')
        verbose_name_plural = _('funcionários')

    def __str__(self):
        return f"{self.nome} ({self.get_cargo_display()})"

class Linha(models.Model):
    """Modelo para as linhas de produção."""
    nome = models.CharField(_('nome da linha'), max_length=100)
    descricao = models.TextField(_('descrição'), blank=True)
    data_criacao = models.DateTimeField(_('data de criação'), auto_now_add=True)
    ativa = models.BooleanField(_('ativa'), default=True)

    class Meta:
        verbose_name = _('linha de produção')
        verbose_name_plural = _('linhas de produção')

    def __str__(self):
        return self.nome

class OrdemProducao(models.Model):
    """Modelo para ordens de produção."""
    class Status(models.TextChoices):
        PENDENTE = 'PENDENTE', _('Pendente')
        EM_PRODUCAO = 'EM_PRODUCAO', _('Em Produção')
        PAUSADA = 'PAUSADA', _('Pausada')
        CONCLUIDA = 'CONCLUIDA', _('Concluída')
        CANCELADA = 'CANCELADA', _('Cancelada')

    numero = models.CharField(_('número da ordem'), max_length=50, unique=True)
    produto = models.CharField(_('produto'), max_length=200)
    quantidade_planejada = models.PositiveIntegerField(_('quantidade planejada'))
    quantidade_produzida = models.PositiveIntegerField(_('quantidade produzida'), default=0)
    linha = models.ForeignKey(Linha, on_delete=models.PROTECT, related_name='ordens')
    responsavel = models.ForeignKey(
        Funcionario, 
        on_delete=models.PROTECT, 
        related_name='ordens_responsavel',
        limit_choices_to={'cargo': Funcionario.Cargo.CHEFE_PRODUCAO}
    )
    data_criacao = models.DateTimeField(_('data de criação'), auto_now_add=True)
    data_inicio = models.DateTimeField(_('data de início'), null=True, blank=True)
    data_conclusao = models.DateTimeField(_('data de conclusão'), null=True, blank=True)
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE
    )
    observacoes = models.TextField(_('observações'), blank=True)

    class Meta:
        verbose_name = _('ordem de produção')
        verbose_name_plural = _('ordens de produção')
        ordering = ['-data_criacao']

    def __str__(self):
        return f"OP {self.numero} - {self.produto}"

class Registro(models.Model):
    """Modelo para registros de produção."""
    class TipoRegistro(models.TextChoices):
        PRODUCAO = 'PRODUCAO', _('Produção')
        PARADA = 'PARADA', _('Parada')
        MANUTENCAO = 'MANUTENCAO', _('Manutenção')
        INSPECAO = 'INSPECAO', _('Inspeção')

    ordem_producao = models.ForeignKey(OrdemProducao, on_delete=models.CASCADE, related_name='registros')
    funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT, related_name='registros')
    tipo = models.CharField(_('tipo de registro'), max_length=20, choices=TipoRegistro.choices)
    data_hora = models.DateTimeField(_('data e hora'), auto_now_add=True)
    quantidade = models.PositiveIntegerField(_('quantidade'), default=0)
    descricao = models.TextField(_('descrição'))
    
    class Meta:
        verbose_name = _('registro')
        verbose_name_plural = _('registros')
        ordering = ['-data_hora']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.ordem_producao} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

class Alerta(models.Model):
    """Modelo para alertas de produção."""
    class Prioridade(models.TextChoices):
        BAIXA = 'BAIXA', _('Baixa')
        MEDIA = 'MEDIA', _('Média')
        ALTA = 'ALTA', _('Alta')
        CRITICA = 'CRITICA', _('Crítica')

    titulo = models.CharField(_('título'), max_length=200)
    descricao = models.TextField(_('descrição'))
    linha = models.ForeignKey(Linha, on_delete=models.CASCADE, related_name='alertas')
    criado_por = models.ForeignKey(Funcionario, on_delete=models.PROTECT, related_name='alertas_criados')
    data_criacao = models.DateTimeField(_('data de criação'), auto_now_add=True)
    prioridade = models.CharField(_('prioridade'), max_length=20, choices=Prioridade.choices)
    resolvido = models.BooleanField(_('resolvido'), default=False)
    data_resolucao = models.DateTimeField(_('data de resolução'), null=True, blank=True)
    resolvido_por = models.ForeignKey(
        Funcionario, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='alertas_resolvidos'
    )
    observacoes_resolucao = models.TextField(_('observações da resolução'), blank=True)

    class Meta:
        verbose_name = _('alerta')
        verbose_name_plural = _('alertas')
        ordering = ['-data_criacao']

    def __str__(self):
        return f"{self.titulo} - {self.get_prioridade_display()}"

class Manutencao(models.Model):
    """Modelo para manutenções de equipamentos."""
    class TipoManutencao(models.TextChoices):
        PREVENTIVA = 'PREVENTIVA', _('Preventiva')
        CORRETIVA = 'CORRETIVA', _('Corretiva')

    class Status(models.TextChoices):
        AGENDADA = 'AGENDADA', _('Agendada')
        EM_ANDAMENTO = 'EM_ANDAMENTO', _('Em Andamento')
        CONCLUIDA = 'CONCLUIDA', _('Concluída')
        CANCELADA = 'CANCELADA', _('Cancelada')

    linha = models.ForeignKey(Linha, on_delete=models.CASCADE, related_name='manutencoes')
    tipo = models.CharField(_('tipo de manutenção'), max_length=20, choices=TipoManutencao.choices)
    descricao = models.TextField(_('descrição'))
    data_agendada = models.DateTimeField(_('data agendada'))
    responsavel = models.ForeignKey(
        Funcionario, 
        on_delete=models.PROTECT, 
        related_name='manutencoes_responsavel',
        limit_choices_to={'cargo': Funcionario.Cargo.MANUTENCAO}
    )
    status = models.CharField(_('status'), max_length=20, choices=Status.choices, default=Status.AGENDADA)
    data_inicio = models.DateTimeField(_('data de início'), null=True, blank=True)
    data_conclusao = models.DateTimeField(_('data de conclusão'), null=True, blank=True)
    observacoes = models.TextField(_('observações'), blank=True)
    duracao_estimada = models.DurationField(_('duração estimada'))
    custo_estimado = models.DecimalField(_('custo estimado'), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = _('manutenção')
        verbose_name_plural = _('manutenções')
        ordering = ['data_agendada']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.linha} - {self.data_agendada.strftime('%d/%m/%Y')}"


class Produto(models.Model):
    """Produtos fabricados."""
    nome = models.CharField(_('nome'), max_length=200)
    codigo = models.CharField(_('código'), max_length=50, unique=True)
    descricao = models.TextField(_('descrição'), blank=True)
    categoria = models.CharField(_('categoria'), max_length=100, blank=True)

    class Meta:
        verbose_name = _('produto')
        verbose_name_plural = _('produtos')

    def __str__(self):
        return f"{self.nome} ({self.codigo})"


class Maquina(models.Model):
    """Máquinas de produção."""
    codigo = models.CharField(_('código identificador'), max_length=50, unique=True)
    foto = models.ImageField(_('foto'), upload_to='maquinas/', null=True, blank=True)
    nome = models.CharField(_('nome'), max_length=150)
    descricao = models.TextField(_('descrição'), blank=True)
    data_criacao = models.DateTimeField(_('data de criação'), auto_now_add=True)

    class Meta:
        verbose_name = _('máquina')
        verbose_name_plural = _('máquinas')

    def __str__(self):
        return f"{self.nome} ({self.codigo})"


class ManutencaoMaquina(models.Model):
    """Histórico de manutenções realizadas em máquinas."""
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name='manutencoes')
    data_hora = models.DateTimeField(_('data/hora da manutenção'), default=timezone.now)
    descricao = models.TextField(_('descrição da manutenção'))
    responsavel = models.ForeignKey(
        Funcionario,
        on_delete=models.PROTECT,
        related_name='manutencoes_realizadas',
        limit_choices_to={'cargo': Funcionario.Cargo.MANUTENCAO}
    )

    class Meta:
        verbose_name = _('manutenção de máquina')
        verbose_name_plural = _('manutenções de máquina')
        ordering = ['-data_hora']

    def __str__(self):
        return f"Manutenção {self.maquina} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"


class Lote(models.Model):
    """Lotes de produção (rastreabilidade com QR code)."""
    codigo = models.CharField(_('código do lote'), max_length=100, unique=True)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='lotes')
    data_hora_inicio = models.DateTimeField(_('data e hora de início'), null=True, blank=True)
    data_hora_final = models.DateTimeField(_('data e hora de finalização'), null=True, blank=True)
    data_inspecao = models.DateTimeField(_('data de inspeção'), null=True, blank=True)
    responsavel_inspecao = models.ForeignKey(
        Funcionario,
        on_delete=models.PROTECT,
        related_name='inspecoes_realizadas',
        null=True,
        blank=True,
        limit_choices_to={'cargo': Funcionario.Cargo.INSPECAO}
    )

    class StatusInspecao(models.TextChoices):
        APROVADO = 'APROVADO', _('Aprovado')
        REPROVADO = 'REPROVADO', _('Reprovado')

    status_inspecao = models.CharField(_('status da inspeção'), max_length=20, choices=StatusInspecao.choices, null=True, blank=True)

    qr_code = models.ImageField(_('QR Code'), upload_to='lotes_qrcodes/', null=True, blank=True)
    observacoes = models.TextField(_('observações'), blank=True)

    class Meta:
        verbose_name = _('lote')
        verbose_name_plural = _('lotes')
        ordering = ['-data_hora_inicio']

    def __str__(self):
        return f"Lote {self.codigo} - {self.produto}"

    def save(self, *args, **kwargs):
        # Gera QR code com as informações básicas do lote se não existir
        if not self.qr_code and self.codigo:
            try:
                import qrcode
                # Conteúdo do QR: pode ser ajustado para incluir URL ou mais metadados
                qr_content = f"LOTE:{self.codigo};PRODUTO:{self.produto.codigo}"
                qr = qrcode.QRCode(version=1, box_size=10, border=4)
                qr.add_data(qr_content)
                qr.make(fit=True)
                img = qr.make_image(fill_color='black', back_color='white')

                # Salvar em memória e atribuir ao ImageField
                buffer = BytesIO()
                img.save(buffer, format='PNG')
                buffer.seek(0)
                file_name = f"{self.codigo}_qrcode.png"
                self.qr_code.save(file_name, ContentFile(buffer.read()), save=False)
            except Exception:
                # Se não houver qrcode/PIL instalados, ignore geração automática
                pass

        super().save(*args, **kwargs)


class ItemProducao(models.Model):
    """Itens individuais produzidos dentro de um lote."""
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='itens')
    data_hora = models.DateTimeField(_('data e hora do item'), default=timezone.now)
    maquina = models.ForeignKey(Maquina, on_delete=models.PROTECT, related_name='itens_produzidos')
    identificador = models.CharField(_('identificação do item'), max_length=200, blank=True)

    class Meta:
        verbose_name = _('item de produção')
        verbose_name_plural = _('itens de produção')
        ordering = ['-data_hora']

    def __str__(self):
        return f"Item {self.identificador or self.pk} - {self.produto} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"