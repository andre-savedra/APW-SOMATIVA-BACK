"""
Script para testar automaticamente a API
Execute: python test_api.py
"""

import requests
import json
import time
import sys
from urllib.parse import urljoin

class APITester:
    def __init__(self, base_url="http://localhost:8000/api"):
        self.base_url = base_url
        self.admin_token = None
        self.user_token = None
        self.session = requests.Session()
        self.test_results = []
        
    def log(self, message, status="INFO"):
        status_icon = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "ERROR": "❌",
            "WARNING": "⚠️"
        }
        print(f"{status_icon.get(status, 'ℹ️')} {message}")
        
    def make_request(self, method, endpoint, data=None, token=None, params=None):
        """Fazer requisição HTTP"""
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))
        headers = {"Content-Type": "application/json"}
        
        if token:
            headers["Authorization"] = f"Bearer {token}"
            
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                headers=headers,
                params=params,
                timeout=30
            )
            return response
        except requests.exceptions.RequestException as e:
            self.log(f"Erro na requisição {method} {url}: {e}", "ERROR")  
            return None
    
    def test_auth_admin(self):
        """Teste 1: Autenticação Admin"""
        self.log("Teste 1: Obtendo token JWT do admin...")
        
        response = self.make_request("POST", "/auth/token/", {
            "username": "admin",
            "password": "admin123"
        })
        
        if response and response.status_code == 200:
            data = response.json()
            self.admin_token = data.get("access")
            self.log("Token admin obtido com sucesso!", "SUCCESS")
            return True
        else:
            self.log(f"Falha na autenticação admin: {response.status_code if response else 'No response'}", "ERROR")
            return False
    
    def test_auth_user(self):
        """Teste 17: Autenticação Usuário Comum"""
        self.log("Teste 17: Obtendo token JWT do usuário comum...")
        
        response = self.make_request("POST", "/auth/token/", {
            "username": "usuario", 
            "password": "usuario123"
        })
        
        if response and response.status_code == 200:
            data = response.json()
            self.user_token = data.get("access")
            self.log("Token usuário obtido com sucesso!", "SUCCESS")
            return True
        else:
            self.log(f"Falha na autenticação usuário: {response.status_code if response else 'No response'}", "ERROR")
            return False
    
    def test_categoria_create(self):
        """Teste 3: Criar Categoria"""
        self.log("Teste 3: Criando categoria...")
        
        response = self.make_request("POST", "/categorias/", {
            "nome": "Games"
        }, self.admin_token)
        
        success = response and response.status_code in [200, 201]
        self.log("Categoria criada!" if success else f"Falha ao criar categoria: {response.status_code if response else 'No response'}", 
                "SUCCESS" if success else "ERROR")
        return success
    
    def test_marca_create(self):
        """Teste 4: Criar Marca"""
        self.log("Teste 4: Criando marca...")
        
        response = self.make_request("POST", "/marcas/", {
            "nome": "PlayStation",
            "cnpj": "11.222.333/0001-44"
        }, self.admin_token)
        
        success = response and response.status_code in [200, 201]
        self.log("Marca criada!" if success else f"Falha ao criar marca: {response.status_code if response else 'No response'}",
                "SUCCESS" if success else "ERROR")
        return success
        
    def test_produto_create(self):
        """Teste 5: Criar Produto"""
        self.log("Teste 5: Criando produto...")
        
        response = self.make_request("POST", "/produtos/", {
            "nome": "PlayStation 5",
            "codigo_registro": "PS5001",
            "codigo_barras": "7899988877766",
            "categoria": 1,
            "marca": 1,
            "custo": "2500.00",
            "valor_venda": "3500.00",
            "informacoes_adicionais": "Console de última geração"
        }, self.admin_token)
        
        success = response and response.status_code in [200, 201]
        self.log("Produto criado!" if success else f"Falha ao criar produto: {response.status_code if response else 'No response'}",
                "SUCCESS" if success else "ERROR")
        return success
    
    def test_produto_list_detailed(self):
        """Teste 6: Listar Produtos com Detalhes"""
        self.log("Teste 6: Listando produtos (verificando detalhes de categoria e marca)...")
        
        response = self.make_request("GET", "/produtos/", token=self.admin_token)
        
        if response and response.status_code == 200:
            data = response.json()
            if "results" in data and len(data["results"]) > 0:
                produto = data["results"][0]
                # Verificar se categoria e marca são objetos, não apenas IDs
                categoria_detalhada = isinstance(produto.get("categoria"), dict)
                marca_detalhada = isinstance(produto.get("marca"), dict)
                
                if categoria_detalhada and marca_detalhada:
                    self.log("Produtos listados com detalhes de categoria e marca!", "SUCCESS")
                    return True
                else:
                    self.log("Produtos não mostram detalhes completos (apenas IDs)", "ERROR")
                    return False
            else:
                self.log("Nenhum produto encontrado na listagem", "WARNING")
                return False
        else:
            self.log(f"Falha ao listar produtos: {response.status_code if response else 'No response'}", "ERROR")
            return False
    
    def test_produto_busca_codigo_barras(self):
        """Teste 7: Busca por Código de Barras (parcial)"""
        self.log("Teste 7: Buscando produtos por código de barras parcial...")
        
        response = self.make_request("GET", "/produtos/buscar-codigo-barras/", 
                                   token=self.admin_token, params={"codigo": "789"})
        
        success = response and response.status_code == 200
        if success:
            data = response.json()
            count = len(data) if isinstance(data, list) else data.get("count", 0)
            self.log(f"Busca por código de barras executada! Encontrados: {count} produtos", "SUCCESS")
        else:
            self.log(f"Falha na busca por código de barras: {response.status_code if response else 'No response'}", "ERROR")
        return success
    
    def test_produto_promocao_list(self):
        """Teste 8: Filtrar Produtos em Promoção"""
        self.log("Teste 8: Filtrando produtos em promoção...")
        
        response = self.make_request("GET", "/produtos/em-promocao/", token=self.admin_token)
        
        success = response and response.status_code == 200
        if success:
            data = response.json()
            count = len(data) if isinstance(data, list) else data.get("count", 0)
            self.log(f"Filtro de promoção executado! Produtos em promoção: {count}", "SUCCESS")
        else:
            self.log(f"Falha ao filtrar produtos em promoção: {response.status_code if response else 'No response'}", "ERROR")
        return success
    
    def test_produto_filtro_setor(self):
        """Teste 9: Filtrar Produtos por Setor"""
        self.log("Teste 9: Filtrando produtos por setor...")
        
        response = self.make_request("GET", "/produtos/", 
                                   token=self.admin_token, params={"setor": "A"})
        
        success = response and response.status_code == 200
        if success:
            data = response.json()
            count = len(data.get("results", [])) if "results" in data else len(data)
            self.log(f"Filtro por setor executado! Produtos no setor A: {count}", "SUCCESS")
        else:
            self.log(f"Falha ao filtrar por setor: {response.status_code if response else 'No response'}", "ERROR")
        return success
    
    def test_produto_ordem_valor_desc(self):
        """Teste 10: Ordenar por Valor (DESC)"""
        self.log("Teste 10: Ordenando produtos por valor (decrescente)...")
        
        response = self.make_request("GET", "/produtos/", 
                                   token=self.admin_token, params={"ordering": "-valor_venda"})
        
        success = response and response.status_code == 200
        self.log("Ordenação por valor (DESC) executada!" if success else f"Falha na ordenação: {response.status_code if response else 'No response'}",
                "SUCCESS" if success else "ERROR")
        return success
    
    def test_produto_ordem_data_asc(self):
        """Teste 11: Ordenar por Data (ASC)"""
        self.log("Teste 11: Ordenando produtos por data (crescente)...")
        
        response = self.make_request("GET", "/produtos/", 
                                   token=self.admin_token, params={"ordering": "data_cadastro"})
        
        success = response and response.status_code == 200
        self.log("Ordenação por data (ASC) executada!" if success else f"Falha na ordenação: {response.status_code if response else 'No response'}",
                "SUCCESS" if success else "ERROR")
        return success
    
    def test_produto_mais_antigos(self):
        """Teste 12: 10 Produtos Mais Antigos"""
        self.log("Teste 12: Buscando 10 produtos mais antigos...")
        
        response = self.make_request("GET", "/produtos/mais-antigos/", token=self.admin_token)
        
        if response and response.status_code == 200:
            data = response.json()
            count = len(data.get("results", []))
            self.log(f"Endpoint dos mais antigos executado! Retornados: {count} produtos", "SUCCESS")
            return True
        else:
            self.log(f"Falha ao buscar produtos mais antigos: {response.status_code if response else 'No response'}", "ERROR")
            return False
    
    def test_setor_create(self):
        """Teste 13: Criar Setor"""
        self.log("Teste 13: Criando setor...")
        
        response = self.make_request("POST", "/setores/", {
            "nome": "F",
            "descricao": "Setor F - Área de Games"
        }, self.admin_token)
        
        success = response and response.status_code in [200, 201]
        self.log("Setor criado!" if success else f"Falha ao criar setor: {response.status_code if response else 'No response'}",
                "SUCCESS" if success else "ERROR")
        return success
    
    def test_setor_list_with_escaninhos(self):
        """Teste 14: Listar Setores com Escaninhos"""
        self.log("Teste 14: Listando setores (verificando se mostra escaninhos)...")
        
        response = self.make_request("GET", "/setores/", token=self.admin_token)
        
        if response and response.status_code == 200:
            data = response.json()
            if "results" in data and len(data["results"]) > 0:
                setor = data["results"][0] 
                tem_escaninhos = "escaninhos" in setor
                self.log("Setores listados com dados dos escaninhos!" if tem_escaninhos else "Setores não mostram escaninhos",
                        "SUCCESS" if tem_escaninhos else "WARNING")
                return tem_escaninhos
            else:
                self.log("Nenhum setor encontrado", "WARNING")
                return False
        else:
            self.log(f"Falha ao listar setores: {response.status_code if response else 'No response'}", "ERROR")
            return False
    
    def test_escaninho_create(self):
        """Teste 15: Criar Escaninho"""
        self.log("Teste 15: Criando escaninho...")
        
        response = self.make_request("POST", "/escaninhos/", {
            "codigo": "999",
            "setor": 1,
            "produto": 1,
            "quantidade": 10
        }, self.admin_token)
        
        success = response and response.status_code in [200, 201]
        self.log("Escaninho criado!" if success else f"Falha ao criar escaninho: {response.status_code if response else 'No response'}",
                "SUCCESS" if success else "ERROR")
        return success
    
    def test_escaninho_list_with_produtos(self):  
        """Teste 16: Listar Escaninhos com Produtos"""
        self.log("Teste 16: Listando escaninhos (verificando se mostra dados dos produtos)...")
        
        response = self.make_request("GET", "/escaninhos/", token=self.admin_token)
        
        if response and response.status_code == 200:
            data = response.json()
            if "results" in data and len(data["results"]) > 0:
                escaninho = data["results"][0]
                produto_detalhado = escaninho.get("produto") and isinstance(escaninho.get("produto"), dict)
                self.log("Escaninhos listados com dados completos dos produtos!" if produto_detalhado else "Escaninhos não mostram detalhes dos produtos",
                        "SUCCESS" if produto_detalhado else "WARNING")
                return produto_detalhado
            else:
                self.log("Nenhum escaninho encontrado", "WARNING")
                return False
        else:
            self.log(f"Falha ao listar escaninhos: {response.status_code if response else 'No response'}", "ERROR")
            return False
    
    def test_promocao_user_forbidden(self):
        """Teste 18: Tentar Promoção com Usuário Comum (DEVE FALHAR)"""
        self.log("Teste 18: Tentando alterar promoção com usuário comum (deve falhar)...")
        
        response = self.make_request("PATCH", "/produtos/1/promocao/", {
            "em_promocao": True
        }, self.user_token)
        
        forbidden = response and response.status_code == 403
        self.log("Usuário comum corretamente bloqueado!" if forbidden else f"ERRO: Usuário comum conseguiu alterar promoção! Status: {response.status_code if response else 'No response'}",
                "SUCCESS" if forbidden else "ERROR")
        return forbidden
    
    def test_promocao_admin_success(self):
        """Teste 19: Alterar Promoção com Admin (DEVE FUNCIONAR)"""
        self.log("Teste 19: Alterando promoção com admin (deve funcionar)...")
        
        response = self.make_request("PATCH", "/produtos/1/promocao/", {
            "em_promocao": True
        }, self.admin_token)
        
        success = response and response.status_code in [200, 201]
        self.log("Admin conseguiu alterar promoção!" if success else f"ERRO: Admin não conseguiu alterar promoção! Status: {response.status_code if response else 'No response'}",
                "SUCCESS" if success else "ERROR")
        return success
    
    def run_all_tests(self):
        """Executar todos os testes na ordem"""
        tests = [
            ("1. Autenticação Admin", self.test_auth_admin),
            ("3. Criar Categoria", self.test_categoria_create),
            ("4. Criar Marca", self.test_marca_create),
            ("5. Criar Produto", self.test_produto_create),
            ("6. Listar Produtos (detalhados)", self.test_produto_list_detailed),
            ("7. Buscar Código de Barras", self.test_produto_busca_codigo_barras),
            ("8. Filtrar Promoções", self.test_produto_promocao_list),
            ("9. Filtrar por Setor", self.test_produto_filtro_setor),
            ("10. Ordenar por Valor DESC", self.test_produto_ordem_valor_desc),
            ("11. Ordenar por Data ASC", self.test_produto_ordem_data_asc),
            ("12. 10 Mais Antigos", self.test_produto_mais_antigos),
            ("13. Criar Setor", self.test_setor_create),
            ("14. Listar Setores (com escaninhos)", self.test_setor_list_with_escaninhos),
            ("15. Criar Escaninho", self.test_escaninho_create),
            ("16. Listar Escaninhos (com produtos)", self.test_escaninho_list_with_produtos),
            ("17. Autenticação Usuário", self.test_auth_user),
            ("18. Promoção Usuário (DEVE FALHAR)", self.test_promocao_user_forbidden),
            ("19. Promoção Admin (DEVE FUNCIONAR)", self.test_promocao_admin_success),
        ]
        
        print("🚀 INICIANDO TESTES DA API - FASE 2")
        print("=" * 50)
        
        passed = 0
        total = len(tests)
        
        for name, test_func in tests:
            print(f"\n▶️ {name}")
            try:
                result = test_func()
                if result:
                    passed += 1
                time.sleep(1)  # Pausa entre testes
            except Exception as e:
                self.log(f"Erro durante o teste: {e}", "ERROR")
        
        print("\n" + "=" * 50)
        print(f"📊 RESULTADO FINAL: {passed}/{total} testes passaram")
        
        if passed == total:
            print("🎉 TODOS OS TESTES PASSARAM! API está funcionando perfeitamente!")
        elif passed >= total * 0.8:
            print("✅ Maioria dos testes passou. Verifique os erros acima.")
        else:
            print("❌ Muitos testes falharam. Verifique a API e tente novamente.")
        
        return passed == total

if __name__ == "__main__":
    # Verificar se a API está rodando
    print("🔍 Verificando se a API está rodando...")
    
    try:
        response = requests.get("http://localhost:8000/api/", timeout=5)
        if response.status_code == 200:
            print("✅ API está rodando!")
        else:
            print("⚠️ API respondeu mas com status diferente de 200")
    except requests.exceptions.RequestException:
        print("❌ API não está rodando! Execute 'python manage.py runserver' primeiro")
        sys.exit(1)
    
    # Executar testes
    tester = APITester()
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)