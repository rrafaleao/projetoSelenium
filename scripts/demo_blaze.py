import time
import random
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service

# Configuração do driver
def setup_driver():
    """Configura e retorna o WebDriver para o Chrome."""
    try:
        service = Service(executable_path="./drivers/chromedriver")
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()
        driver.implicitly_wait(10)  # Espera implícita de 10 segundos
        print("✅ Driver do Chrome inicializado com sucesso.")
        return driver
    except Exception as e:
        print(f"❌ Erro ao inicializar o driver: {str(e)}")
        raise

def log_step(step_number, description, success=True):
    """Registra um passo do teste no console."""
    status = "✅" if success else "❌"
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] Passo {step_number}: {description} {status}")

def main():
    """Função principal que executa o caso de teste."""
    results = {
        "id": "TC-004",
        "title": "Simulação de compra no demoblaze.com",
        "objective": "Simular uma compra de um produto qualquer no site demoblaze.com",
        "steps": [],
        "input_data": {},
        "expected_result": "Compra realizada com sucesso, com modal de confirmação exibindo ID do pedido e valor",
        "actual_result": "",
        "status": "Falhou",  # Assume falha inicialmente
        "error": None
    }
    
    driver = None
    
    try:
        # Passo 1: Configurar e iniciar o WebDriver
        driver = setup_driver()
        results["steps"].append({
            "number": 1,
            "description": "Iniciar o WebDriver e maximizar a janela",
            "status": "Passou"
        })
        
        # Passo 2: Navegar para o site demoblaze.com
        driver.get("https://www.demoblaze.com/")
        log_step(2, "Navegar para https://www.demoblaze.com/")
        results["steps"].append({
            "number": 2,
            "description": "Navegar para o site demoblaze.com",
            "status": "Passou"
        })
        
        # Passo 3: Esperar o carregamento da página e escolher um produto
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".card-title"))
        )
        
        # Selecionar um produto aleatório
        produtos = driver.find_elements(By.CSS_SELECTOR, ".card-title a")
        if not produtos:
            raise Exception("Nenhum produto encontrado na página")
            
        produto_escolhido = random.choice(produtos)
        nome_produto = produto_escolhido.text
        log_step(3, f"Produto escolhido: {nome_produto}")
        results["input_data"]["produto"] = nome_produto
        produto_escolhido.click()
        
        results["steps"].append({
            "number": 3,
            "description": f"Escolher um produto: {nome_produto}",
            "status": "Passou"
        })
        
        # Passo 4: Adicionar ao carrinho
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-success"))
        )
        add_to_cart_btn = driver.find_element(By.CSS_SELECTOR, ".btn-success")
        add_to_cart_btn.click()
        log_step(4, "Clicar no botão 'Add to cart'")
        
        # Esperar e aceitar o alerta
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            log_step(4.1, f"Alerta aceito: '{alert_text}'")
        except TimeoutException:
            log_step(4.1, "Nenhum alerta foi exibido", success=False)
        
        results["steps"].append({
            "number": 4,
            "description": "Adicionar produto ao carrinho e aceitar alerta",
            "status": "Passou"
        })
        
        # Passo 5: Navegar para o carrinho
        time.sleep(2)  # Pequena pausa para garantir que o alerta foi processado
        cart_link = driver.find_element(By.ID, "cartur")
        cart_link.click()
        log_step(5, "Navegar para o carrinho")
        
        results["steps"].append({
            "number": 5,
            "description": "Navegar para o carrinho",
            "status": "Passou"
        })
        
        # Passo 6: Verificar se o produto está no carrinho e finalizar a compra
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".success"))
        )
        
        produtos_carrinho = driver.find_elements(By.CSS_SELECTOR, ".success td:nth-child(2)")
        if not any(nome_produto == p.text for p in produtos_carrinho):
            log_step(6, "Produto não encontrado no carrinho", success=False)
            raise Exception(f"Produto '{nome_produto}' não encontrado no carrinho")
            
        place_order_btn = driver.find_element(By.CSS_SELECTOR, ".btn-success")
        place_order_btn.click()
        log_step(6, "Clicar em 'Place Order'")
        
        results["steps"].append({
            "number": 6,
            "description": "Verificar produto no carrinho e clicar em 'Place Order'",
            "status": "Passou"
        })
        
        # Passo 7: Preencher formulário de pedido
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "name"))
        )
        
        # Dados para o formulário
        form_data = {
            "name": "Cliente Teste",
            "country": "Brasil",
            "city": "São Paulo",
            "card": "4111111111111111",
            "month": "12",
            "year": "2025"
        }
        results["input_data"]["form_data"] = form_data
        
        # Preencher cada campo
        for field_id, value in form_data.items():
            input_field = driver.find_element(By.ID, field_id)
            input_field.clear()
            input_field.send_keys(value)
            log_step(7, f"Preencher '{field_id}' com '{value}'")
        
        results["steps"].append({
            "number": 7,
            "description": "Preencher formulário de pedido com dados válidos",
            "status": "Passou"
        })
        
        # Passo 8: Confirmar a compra
        purchase_btn = driver.find_element(By.CSS_SELECTOR, "#orderModal .btn-primary")
        purchase_btn.click()
        log_step(8, "Clicar em 'Purchase'")
        
        results["steps"].append({
            "number": 8,
            "description": "Confirmar a compra clicando em 'Purchase'",
            "status": "Passou"
        })
        
        # Passo 9: Verificar a confirmação da compra
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".sweet-alert h2"))
        )
        
        confirmation_header = driver.find_element(By.CSS_SELECTOR, ".sweet-alert h2").text
        confirmation_details = driver.find_element(By.CSS_SELECTOR, ".sweet-alert p.lead").text
        
        # Extrair ID do pedido e valor total
        lines = confirmation_details.split('\n')
        order_id = next((line.split(':')[1].strip() for line in lines if 'Id' in line), "Não encontrado")
        amount = next((line.split(':')[1].strip() for line in lines if 'Amount' in line), "Não encontrado")
        
        log_step(9, f"Compra confirmada: ID {order_id}, Valor {amount}")
        
        results["actual_result"] = f"Compra realizada com sucesso. Confirmação: '{confirmation_header}'. ID do pedido: {order_id}, Valor: {amount}"
        results["status"] = "Passou"
        
        results["steps"].append({
            "number": 9,
            "description": "Verificar confirmação da compra",
            "status": "Passou"
        })
        
        # Passo 10: Finalizar o teste
        ok_btn = driver.find_element(By.CSS_SELECTOR, ".confirm")
        ok_btn.click()
        log_step(10, "Clicar em 'OK' para concluir")
        
        results["steps"].append({
            "number": 10,
            "description": "Clicar em 'OK' para concluir o processo",
            "status": "Passou"
        })
        
    except Exception as e:
        error_msg = str(e)
        log_step("ERRO", error_msg, success=False)
        results["error"] = error_msg
        results["actual_result"] = f"Falha durante a execução: {error_msg}"
    
    finally:
        # Finalizar o teste fechando o navegador
        if driver:
            driver.quit()
            log_step("FIM", "Navegador fechado")
        
        # Imprimir resumo do teste
        print("\n" + "="*50)
        print(f"RESULTADO DO TESTE: {results['status']}")
        if results['status'] == 'Passou':
            print(f"Resultado obtido: {results['actual_result']}")
        else:
            print(f"Erro: {results['error']}")
        print("="*50)
        
        return results

if __name__ == "__main__":
    main()