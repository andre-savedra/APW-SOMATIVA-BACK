"""
Script para popular o banco de dados com dados de teste
Execute: python manage.py shell < populate_db.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from estoque.models import Categoria, Marca, Setor, Produto, Escaninho
from decimal import Decimal
import random

def create_sample_data():
    print("🗃️ Criando dados de exemplo...")
    
    # Criar usuário admin se não existir
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("✅ Usuário admin criado")
    
    # Criar usuário comum
    if not User.objects.filter(username='usuario').exists():
        User.objects.create_user('usuario', 'usuario@example.com', 'usuario123')
        print("✅ Usuário comum criado")
    
    # Categorias
    categorias_data = [
        'Eletrônicos', 'Roupas', 'Casa e Jardim', 'Esportes', 
        'Livros', 'Beleza', 'Automotivo', 'Ferramentas'
    ]
    
    categorias = []
    for nome in categorias_data:
        categoria, created = Categoria.objects.get_or_create(nome=nome)
        categorias.append(categoria)
        if created:
            print(f"✅ Categoria '{nome}' criada")
    
    # Marcas
    marcas_data = [
        ('Samsung', '12.345.678/0001-90'),
        ('Apple', '23.456.789/0001-91'),
        ('Nike', '34.567.890/0001-92'),
        ('Adidas', '45.678.901/0001-93'),
        ('Sony', '56.789.012/0001-94'),
        ('LG', '67.890.123/0001-95'),
        ('Microsoft', '78.901.234/0001-96'),
        ('Dell', '89.012.345/0001-97'),
    ]
    
    marcas = []
    for nome, cnpj in marcas_data:
        marca, created = Marca.objects.get_or_create(
            nome=nome,
            defaults={'cnpj': cnpj}
        )
        marcas.append(marca)
        if created:
            print(f"✅ Marca '{nome}' criada")
    
    # Setores
    setores_data = ['A', 'B', 'C', 'D', 'E']
    setores = []
    for nome in setores_data:
        setor, created = Setor.objects.get_or_create(
            nome=nome,
            defaults={'descricao': f'Setor {nome} - Área de armazenamento'}
        )
        setores.append(setor)
        if created:
            print(f"✅ Setor '{nome}' criado")
    
    # Produtos
    produtos_data = [
        ('Smartphone Galaxy S23', '001', '7891234567890'),
        ('iPhone 15 Pro', '002', '7891234567891'),
        ('Tênis Air Max', '003', '7891234567892'),
        ('Camiseta Adidas', '004', '7891234567893'),
        ('TV LED 55"', '005', '7891234567894'),
        ('Notebook Dell', '006', '7891234567895'),
        ('Mouse Gamer', '007', '7891234567896'),
        ('Fone Bluetooth', '008', '7891234567897'),
        ('Tablet Samsung', '009', '7891234567898'),
        ('Smartwatch Apple', '010', '7891234567899'),
    ]
    
    admin_user = User.objects.get(username='admin')
    produtos = []
    
    for i, (nome, codigo, barras) in enumerate(produtos_data):
        if not Produto.objects.filter(codigo_registro=codigo).exists():
            categoria = random.choice(categorias)
            marca = random.choice(marcas)
            custo = Decimal(str(random.uniform(50, 500)))
            valor_venda = custo * Decimal('1.3')  # 30% de margem
            
            produto = Produto.objects.create(
                nome=nome,
                codigo_registro=codigo,
                codigo_barras=barras,
                categoria=categoria,
                marca=marca,
                custo=custo,
                valor_venda=valor_venda,
                informacoes_adicionais=f"Produto de exemplo número {i+1}",
                em_promocao=random.choice([True, False]) if i % 3 == 0 else False,
                criado_por=admin_user
            )
            produtos.append(produto)
            print(f"✅ Produto '{nome}' criado")
    
    # Escaninhos
    escaninho_counter = 1
    for setor in setores:
        for i in range(1, 6):  # 5 escaninhos por setor
            codigo = str(escaninho_counter).zfill(3)
            
            if not Escaninho.objects.filter(setor=setor, codigo=codigo).exists():
                # 70% dos escaninhos têm produtos
                tem_produto = random.random() < 0.7
                produto = random.choice(produtos) if tem_produto and produtos else None
                quantidade = random.randint(1, 50) if produto else 0
                
                escaninho = Escaninho.objects.create(
                    codigo=codigo,
                    setor=setor,
                    produto=produto,
                    quantidade=quantidade
                )
                print(f"✅ Escaninho {setor.nome}-{codigo} criado")
            
            escaninho_counter += 1
    
    print("\n🎉 Dados de exemplo criados com sucesso!")
    print(f"📊 Resumo:")
    print(f"   • {Categoria.objects.count()} categorias")
    print(f"   • {Marca.objects.count()} marcas")
    print(f"   • {Setor.objects.count()} setores")
    print(f"   • {Produto.objects.count()} produtos")
    print(f"   • {Escaninho.objects.count()} escaninhos")
    print(f"   • {Produto.objects.filter(em_promocao=True).count()} produtos em promoção")

if __name__ == '__main__':
    create_sample_data()