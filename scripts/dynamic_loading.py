import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Informações do caso de teste
TEST_ID = "TC-003"
TEST_TITLE = "Teste de Carregamento Dinâmico"
TEST_OBJECTIVE = "Verificar se o texto 'Hello World!' aparece após clicar no botão 'Start'"

def execute_test():
    """Executa o caso de teste TC-003 para validar o carregamento dinâmico"""
    
    driver = None
    test_result = {
        "test_id": TEST_ID,
        "test_title": TEST_TITLE,
        "objective": TEST_OBJECTIVE,
        "steps_executed": [],
        "expected_result": "O texto 'Hello World!' deve aparecer após o carregamento",
        "actual_result": "",
        "status": "Falhou",  # Assume falha por padrão
        "execution_time": 0
    }
    
    start_time = time.time()
    
    try:
        # Passo 1: Inicializar o navegador
        logger.info("Inicializando o navegador Chrome")
        test_result["steps_executed"].append("1. Inicializar o navegador Chrome")
        
        # Cria uma instância do Chrome WebDriver
        driver = webdriver.Chrome()
        driver.maximize_window()
        
        # Passo 2: Navegar para a página de teste
        logger.info("Navegando para a página de carregamento dinâmico")
        test_result["steps_executed"].append("2. Navegar para https://the-internet.herokuapp.com/dynamic_loading/1")
        
        driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")
        
        # Passo 3: Localizar e clicar no botão Start
        logger.info("Localizando e clicando no botão 'Start'")
        test_result["steps_executed"].append("3. Localizar e clicar no botão 'Start'")
        
        start_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Start')]")
        start_button.click()
        
        # Passo 4: Aguardar o carregamento do texto usando Explicit Wait
        logger.info("Aguardando o carregamento do texto 'Hello World!'")
        test_result["steps_executed"].append("4. Aguardar o carregamento do texto 'Hello World!' (timeout: 30s)")
        
        wait_start = time.time()
        
        wait = WebDriverWait(driver, 30)
        hello_element = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[@id='finish']/h4"))
        )
        
        wait_time = time.time() - wait_start
        
        # Passo 5: Verificar se o texto está correto
        logger.info("Verificando se o texto exibido é 'Hello World!'")
        test_result["steps_executed"].append("5. Verificar se o texto exibido é 'Hello World!'")
        
        actual_text = hello_element.text
        expected_text = "Hello World!"
        
        if actual_text == expected_text:
            logger.info(f"Teste passou! Texto encontrado: '{actual_text}'")
            test_result["status"] = "Passou"
            test_result["actual_result"] = f"O texto '{actual_text}' foi exibido após {wait_time:.2f} segundos de espera"
        else:
            logger.error(f"Texto incorreto. Esperado: '{expected_text}', Obtido: '{actual_text}'")
            test_result["status"] = "Falhou"
            test_result["actual_result"] = f"Texto incorreto. Esperado: '{expected_text}', Obtido: '{actual_text}'"
    
    except TimeoutException:
        logger.error("Timeout: O elemento não apareceu no tempo especificado")
        test_result["status"] = "Falhou"
        test_result["actual_result"] = "Timeout: O texto 'Hello World!' não apareceu dentro do tempo limite de 30 segundos"
    
    except WebDriverException as e:
        logger.error(f"Erro no WebDriver: {str(e)}")
        test_result["status"] = "Falhou"
        test_result["actual_result"] = f"Erro no WebDriver: {str(e)}"
    
    except Exception as e:
        logger.error(f"Erro não esperado: {str(e)}")
        test_result["status"] = "Falhou"
        test_result["actual_result"] = f"Erro não esperado: {str(e)}"
    
    finally:
        # Finaliza o teste e fecha o navegador
        test_result["execution_time"] = time.time() - start_time
        
        if driver:
            logger.info("Fechando o navegador")
            test_result["steps_executed"].append("6. Fechar o navegador")
            driver.quit()
        
        # Exibe o resultado do teste
        logger.info(f"Resultado do teste {TEST_ID}: {test_result['status']}")
        logger.info(f"Tempo total de execução: {test_result['execution_time']:.2f} segundos")
        
        return test_result

if __name__ == "__main__":
    result = execute_test()
    
    # Imprime o resultado formatado
    print("\n" + "="*80)
    print(f"RELATÓRIO DE TESTE: {result['test_id']} - {result['test_title']}")
    print("="*80)
    print(f"Objetivo: {result['objective']}")
    print("\nPassos Executados:")
    for step in result['steps_executed']:
        print(f"  {step}")
    print(f"\nResultado Esperado: {result['expected_result']}")
    print(f"Resultado Obtido: {result['actual_result']}")
    print(f"Status: {result['status']}")
    print(f"Tempo de Execução: {result['execution_time']:.2f} segundos")
    print("="*80 + "\n")