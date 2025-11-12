import requests

# Testar login admin
response = requests.post('http://localhost:8000/api/auth/token/', json={
    'username': 'admin',
    'password': 'admin123'
})

print(f"Status Admin: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Token Admin: {data.get('access')[:50]}...")
else:
    print(f"Erro Admin: {response.text}")

# Testar login usuário
response = requests.post('http://localhost:8000/api/auth/token/', json={
    'username': 'usuario', 
    'password': 'usuario123'
})

print(f"Status Usuário: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Token Usuário: {data.get('access')[:50]}...")
else:
    print(f"Erro Usuário: {response.text}")