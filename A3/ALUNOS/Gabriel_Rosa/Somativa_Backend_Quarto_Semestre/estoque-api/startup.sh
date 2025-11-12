#!/bin/bash

echo "🚀 Iniciando API de Estoque no Azure..."

# Instalar dependências
echo "📦 Instalando dependências..."
python -m pip install --upgrade pip
pip install -r requirements.txt

# Coletar arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Executar migrações
echo "🗃️ Executando migrações..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "✅ Configuração concluída!"

# Iniciar servidor
echo "🌐 Iniciando servidor..."
gunicorn --bind 0.0.0.0:8000 --workers 4 config.wsgi:application