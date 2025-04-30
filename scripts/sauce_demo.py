import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def log_test_step(step_desc):
    """Função para registrar passos de teste com timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {step_desc}")

def execute_test_case_001():
    """
    TC-001: Login bem-sucedido com usuário padrão (standard_user/secret_sauce)
    """
    start_time = datetime.now()
    log_test_step("Iniciando TC-001: Login bem-sucedido")
    
    # Configurar o driver (assumindo Chrome)
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    try:
        # Passo 1: Acessar o site
        log_test_step("Passo 1: Acessando o site SauceDemo")
        driver.get("https://www.saucedemo.com/")
        
        # Passo 2: Inserir credenciais válidas
        log_test_step("Passo 2: Inserindo credenciais válidas (standard_user/secret_sauce)")
        username_field = driver.find_element(By.ID, "user-name")
        password_field = driver.find_element(By.ID, "password")
        
        username_field.send_keys("standard_user")
        password_field.send_keys("secret_sauce")
        
        # Passo 3: Clicar no botão de login
        log_test_step("Passo 3: Clicando no botão de login")
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()
        
        # Passo 4: Verificar se o login foi bem-sucedido (redirecionamento para página de produtos)
        log_test_step("Passo 4: Verificando se o login foi bem-sucedido")
        
        # Aguardar até que a página de produtos seja carregada (verificando a existência do elemento inventory_container)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "inventory_container"))
        )
        
        # Verificar URL da página após o login
        current_url = driver.current_url
        expected_url = "https://www.saucedemo.com/inventory.html"
        
        if current_url == expected_url:
            log_test_step("✅ Teste PASSOU: Login bem-sucedido, página de produtos exibida")
            result = "PASSOU"
        else:
            log_test_step("❌ Teste FALHOU: URL incorreta após login")
            result = "FALHOU"
            
    except (NoSuchElementException, TimeoutException) as e:
        log_test_step(f"❌ Teste FALHOU: {str(e)}")
        result = "FALHOU"
    finally:
        # Capturar screenshot final (opcional)
        driver.save_screenshot("images/tc001_resultado.png")
        
        # Fechar o navegador
        driver.quit()
        
        end_time = datetime.now()
        duration = end_time - start_time
        log_test_step(f"Teste TC-001 finalizado. Duração: {duration}")
        
        return {
            "id": "TC-001",
            "titulo": "Login bem-sucedido com usuário padrão",
            "resultado": result,
            "inicio": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "fim": end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "duracao": str(duration)
        }

def execute_test_case_002():
    """
    TC-002: Login mal-sucedido com usuário inválido
    """
    start_time = datetime.now()
    log_test_step("Iniciando TC-002: Login mal-sucedido")
    
    # Configurar o driver (assumindo Chrome)
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    try:
        # Passo 1: Acessar o site
        log_test_step("Passo 1: Acessando o site SauceDemo")
        driver.get("https://www.saucedemo.com/")
        
        # Passo 2: Inserir credenciais inválidas
        log_test_step("Passo 2: Inserindo credenciais inválidas (invalid_user/wrong_password)")
        username_field = driver.find_element(By.ID, "user-name")
        password_field = driver.find_element(By.ID, "password")
        
        username_field.send_keys("invalid_user")
        password_field.send_keys("wrong_password")
        
        # Passo 3: Clicar no botão de login
        log_test_step("Passo 3: Clicando no botão de login")
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()
        
        # Passo 4: Verificar se a mensagem de erro aparece
        log_test_step("Passo 4: Verificando se a mensagem de erro é exibida")
        
        # Aguardar até que a mensagem de erro seja exibida
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".error-message-container.error"))
        )
        
        # Verificar o conteúdo da mensagem de erro
        error_text = error_message.text
        expected_error = "Epic sadface: Username and password do not match any user in this service"
        
        if expected_error in error_text:
            log_test_step(f"✅ Teste PASSOU: Mensagem de erro correta exibida: '{error_text}'")
            result = "PASSOU"
        else:
            log_test_step(f"❌ Teste FALHOU: Mensagem de erro incorreta: '{error_text}'")
            result = "FALHOU"
            
    except (NoSuchElementException, TimeoutException) as e:
        log_test_step(f"❌ Teste FALHOU: {str(e)}")
        result = "FALHOU"
    finally:
        driver.save_screenshot("images/tc002_resultado.png")
        driver.quit()
        
        end_time = datetime.now()
        duration = end_time - start_time
        log_test_step(f"Teste TC-002 finalizado. Duração: {duration}")
        
        return {
            "id": "TC-002",
            "titulo": "Login mal-sucedido com usuário inválido",
            "resultado": result,
            "inicio": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "fim": end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "duracao": str(duration),
            "erro": error_text if result == "FALHOU" else None
        }

if __name__ == "__main__":
    # Executar ambos os casos de teste
    resultado_tc001 = execute_test_case_001()
    time.sleep(1)  # Breve pausa entre os testes
    resultado_tc002 = execute_test_case_002()
    
    # Imprimir resumo dos resultados
    print("\n===== RESUMO DOS TESTES =====")
    print(f"TC-001: {resultado_tc001['resultado']} - {resultado_tc001['titulo']}")
    print(f"TC-002: {resultado_tc002['resultado']} - {resultado_tc002['titulo']}")
    print("=============================")