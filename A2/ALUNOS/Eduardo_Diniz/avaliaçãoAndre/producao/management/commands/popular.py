from django.core.management.base import BaseCommand
from producao.models import *
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Popula o banco com dados de teste'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Iniciando população de dados...\n')

        # Criar funcionários de diferentes cargos
        self.stdout.write('👥 Criando funcionários...')
        
        func_prod = Funcionario.objects.create_user(
            username='joao_prod',
            email='joao@empresa.com',
            password='senha123',
            numero_registro='PROD001',
            cpf='111.111.111-11',
            data_contratacao=timezone.now().date(),
            cargo='PRODUCAO',
            first_name='João',
            last_name='Silva'
        )
        self.stdout.write(f'  ✓ {func_prod.username} - PRODUCAO')

        func_lider = Funcionario.objects.create_user(
            username='maria_lider',
            email='maria@empresa.com',
            password='senha123',
            numero_registro='LID001',
            cpf='222.222.222-22',
            data_contratacao=timezone.now().date(),
            cargo='LIDER_PRODUCAO',
            first_name='Maria',
            last_name='Santos'
        )
        self.stdout.write(f'  ✓ {func_lider.username} - LIDER_PRODUCAO')

        func_insp = Funcionario.objects.create_user(
            username='carlos_insp',
            email='carlos@empresa.com',
            password='senha123',
            numero_registro='INSP001',
            cpf='333.333.333-33',
            data_contratacao=timezone.now().date(),
            cargo='INSPECAO',
            first_name='Carlos',
            last_name='Oliveira'
        )
        self.stdout.write(f'  ✓ {func_insp.username} - INSPECAO')

        func_manut = Funcionario.objects.create_user(
            username='pedro_manut',
            email='pedro@empresa.com',
            password='senha123',
            numero_registro='MAN001',
            cpf='444.444.444-44',
            data_contratacao=timezone.now().date(),
            cargo='MANUTENCAO',
            first_name='Pedro',
            last_name='Costa'
        )
        self.stdout.write(f'  ✓ {func_manut.username} - MANUTENCAO\n')

        # Criar produtos
        self.stdout.write('📦 Criando produtos...')
        produtos = []
        categorias = ['Eletrônicos', 'Mecânicos', 'Plásticos']
        
        for i, cat in enumerate(categorias, 1):
            prod = Produto.objects.create(
                nome=f'Produto {cat} {i}',
                codigo=f'PROD{i:03d}',
                descricao=f'Descrição do produto {i}',
                categoria=cat
            )
            produtos.append(prod)
            self.stdout.write(f'  ✓ {prod.codigo} - {prod.nome}')

        # Criar máquinas
        self.stdout.write('\n🏭 Criando máquinas...')
        maquinas = []
        for i in range(1, 4):
            maq = Maquina.objects.create(
                codigo=f'MAQ{i:03d}',
                nome=f'Máquina CNC {i}',
                descricao=f'Máquina de produção tipo {i}'
            )
            maquinas.append(maq)
            self.stdout.write(f'  ✓ {maq.codigo} - {maq.nome}')

        # Criar manutenções
        self.stdout.write('\n🔧 Criando manutenções...')
        for maq in maquinas:
            Manutencao.objects.create(
                maquina=maq,
                data_hora=timezone.now() - timedelta(days=30),
                descricao='Manutenção preventiva',
                funcionario=func_manut
            )
        self.stdout.write(f'  ✓ {Manutencao.objects.count()} manutenções criadas')

        # Criar lotes e itens
        self.stdout.write('\n📊 Criando lotes e itens...')
        for i in range(1, 6):
            lote = Lote.objects.create(
                codigo=f'LOTE{i:03d}',
                data_inicio=timezone.now() - timedelta(days=i*2),
                data_fim=timezone.now() - timedelta(days=i*2-1),
            )
            
            if i % 2 == 0:
                lote.data_inspecao = timezone.now() - timedelta(days=i*2-1)
                lote.responsavel_inspecao = func_insp
                lote.status_inspecao = 'Aprovado' if i % 4 == 0 else 'Reprovado'
                lote.save()

            for j in range(1, 11):
                ItemProducao.objects.create(
                    lote=lote,
                    produto=produtos[j % len(produtos)],
                    maquina=maquinas[j % len(maquinas)],
                    data_hora=timezone.now() - timedelta(days=i*2, hours=j)
                )
            
            self.stdout.write(f'  ✓ {lote.codigo} com 10 itens')

        self.stdout.write(self.style.SUCCESS('\n✅ Dados populados com sucesso!'))
        self.stdout.write('\n📊 RESUMO:')
        self.stdout.write(f'   Funcionários: {Funcionario.objects.count()}')
        self.stdout.write(f'   Produtos: {Produto.objects.count()}')
        self.stdout.write(f'   Máquinas: {Maquina.objects.count()}')
        self.stdout.write(f'   Manutenções: {Manutencao.objects.count()}')
        self.stdout.write(f'   Lotes: {Lote.objects.count()}')
        self.stdout.write(f'   Itens: {ItemProducao.objects.count()}')
        
        self.stdout.write('\n👥 USUÁRIOS DE TESTE:')
        self.stdout.write('   joao_prod    | senha123 | PRODUCAO')
        self.stdout.write('   maria_lider  | senha123 | LIDER_PRODUCAO')
        self.stdout.write('   carlos_insp  | senha123 | INSPECAO')
        self.stdout.write('   pedro_manut  | senha123 | MANUTENCAO')