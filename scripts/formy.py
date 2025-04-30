import time
import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='relatorios/tc_formy_log.txt',
    filemode='w'
)
logger = logging.getLogger(__name__)

# Configuração do driver
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Executar em modo headless se necessário
chrome_options.add_argument("--window-size=1920,1080")
chrome_service = Service('../drivers/chromedriver')  # Ajuste o caminho conforme necessário
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Maximizar a janela
driver.maximize_window()

# Certifique-se de que o diretório de screenshots exista
if not os.path.exists('../images'):
    os.makedirs('../images')

def main():
    form_data = {}  # Dicionário para armazenar os valores inseridos no formulário
    try:
        # TC-005: Preencher todos os campos do formulário e submeter
        logger.info("INICIANDO CASO DE TESTE TC-005: Preenchimento completo do formulário")
        
        # Passo 1: Acessar o site do formulário
        url = "https://formy-project.herokuapp.com/form"
        logger.info(f"Acessando o site: {url}")
        driver.get(url)
        
        # Aguardar carregamento da página
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.ID, "first-name")))
        logger.info("Página do formulário carregada com sucesso")
        
        # Tirar screenshot inicial
        driver.save_screenshot('../images/tc005_formulario_inicial.png')
        logger.info("Screenshot inicial salvo")
        
        # Passo 2: Preencher campos de texto
        logger.info("Preenchendo campos de texto")
        
        # Nome (usando ID)
        first_name = "João"
        first_name_field = driver.find_element(By.ID, "first-name")
        first_name_field.send_keys(first_name)
        form_data["Nome"] = first_name
        
        # Sobrenome (usando NAME)
        last_name = "Silva"
        last_name_field = driver.find_element(By.ID, "last-name")
        last_name_field.send_keys(last_name)
        form_data["Sobrenome"] = last_name
        
        # Cargo (usando xpath)
        job_title = "Engenheiro de Automação"
        job_title_field = driver.find_element(By.XPATH, "//input[@id='job-title']")
        job_title_field.send_keys(job_title)
        form_data["Cargo"] = job_title
        
        # Passo 3: Selecionar opções de rádio para educação (usando CSS Selector)
        logger.info("Selecionando nível de educação")
        education_level = "College"
        education_radio = driver.find_element(By.CSS_SELECTOR, "input#radio-button-2")
        education_radio.click()
        form_data["Educação"] = education_level
        
        # Passo 4: Selecionar opções de gênero (usando ID)
        logger.info("Selecionando gênero")
        gender = "Masculino"
        gender_radio = driver.find_element(By.ID, "radio-button-1")
        gender_radio.click()
        form_data["Gênero"] = gender
        
        # Passo 5: Selecionar opções de experiência (checkboxes)
        logger.info("Selecionando anos de experiência")
        experience = "2-4"
        experience_checkbox = driver.find_element(By.CSS_SELECTOR, "input#checkbox-2")
        experience_checkbox.click()
        form_data["Experiência"] = experience
        
        # Passo 6: Selecionar data (usando ID)
        logger.info("Preenchendo data")
        date_input = driver.find_element(By.ID, "datepicker")
        date_value = "01/15/2023"
        date_input.send_keys(date_value)
        # Clicar fora para fechar o datepicker
        driver.find_element(By.TAG_NAME, "body").click()
        form_data["Data"] = date_value
        
        # Passo 7: Preencher o telefone (usando ID)
        logger.info("Preenchendo telefone")
        phone = "(11) 99999-9999"
        phone_field = driver.find_element(By.ID, "phone")
        phone_field.send_keys(phone)
        form_data["Telefone"] = phone
        
        # Passo 8: Preencher o email (usando ID)
        logger.info("Preenchendo email")
        email = "joao.silva@exemplo.com"
        email_field = driver.find_element(By.ID, "email")
        email_field.send_keys(email)
        form_data["Email"] = email
        
        # Passo 9: Preencher endereço (usando ID)
        logger.info("Preenchendo endereço")
        address = "Av. Paulista, 1000"
        address_field = driver.find_element(By.ID, "address")
        address_field.send_keys(address)
        form_data["Endereço"] = address
        
        # Passo 10: Preencher cidade (usando ID)
        logger.info("Preenchendo cidade")
        city = "São Paulo"
        city_field = driver.find_element(By.ID, "city")
        city_field.send_keys(city)
        form_data["Cidade"] = city
        
        # Passo 11: Preencher estado (usando ID)
        logger.info("Preenchendo estado")
        state = "SP"
        state_field = driver.find_element(By.ID, "state")
        state_field.send_keys(state)
        form_data["Estado"] = state
        
        # Passo 12: Preencher CEP (usando ID)
        logger.info("Preenchendo CEP")
        zip_code = "01310-100"
        zip_field = driver.find_element(By.ID, "zip")
        zip_field.send_keys(zip_code)
        form_data["CEP"] = zip_code
        
        # Passo 13: Tirar screenshot do formulário preenchido
        driver.save_screenshot('../images/tc005_formulario_preenchido.png')
        logger.info("Screenshot do formulário preenchido salvo")
        
        # Passo 14: Submeter o formulário (usando CSS Selector)
        logger.info("Submetendo o formulário")
        submit_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary")
        submit_button.click()
        
        # Passo 15: Verificar página de sucesso
        try:
            # Aguardar até que o elemento de sucesso esteja visível
            success_message = wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "alert-success"))
            )
            
            # Obter o texto da mensagem de sucesso
            success_text = success_message.text
            logger.info(f"Mensagem de sucesso: {success_text}")
            
            # Tirar screenshot da página de sucesso
            driver.save_screenshot('../images/tc005_sucesso.png')
            logger.info("Screenshot da página de sucesso salvo")
            
            # Verificar se o envio foi bem-sucedido
            if "The form was successfully submitted!" in success_text:
                logger.info("TESTE PASSOU: Formulário enviado com sucesso")
                test_result = "PASSOU"
            else:
                logger.error("TESTE FALHOU: Mensagem de sucesso incorreta")
                test_result = "FALHOU"
                
        except TimeoutException:
            logger.error("TESTE FALHOU: Tempo esgotado aguardando a mensagem de sucesso")
            test_result = "FALHOU"
        
        # Resultado final
        return {
            "test_id": "TC-005",
            "status": test_result,
            "form_data": form_data,
            "success_message": success_text if 'success_text' in locals() else "N/A"
        }
        
    except Exception as e:
        logger.error(f"Erro na execução do teste: {str(e)}")
        return {
            "test_id": "TC-005",
            "status": "FALHOU",
            "error": str(e),
            "form_data": form_data  # Retorna os dados preenchidos até o momento do erro
        }
    finally:
        # Fechar o navegador
        driver.quit()
        logger.info("Navegador fechado")

if __name__ == "__main__":
    result = main()
    print(f"\nResultado do teste {result['test_id']}: {result['status']}")
    
    if result['status'] == "PASSOU":
        print("\nDados preenchidos no formulário:")
        for field, value in result['form_data'].items():
            print(f"- {field}: {value}")
        print(f"\nMensagem de sucesso: {result.get('success_message', 'N/A')}")
    else:
        print(f"Erro: {result.get('error', 'Erro desconhecido')}")
        print("\nDados preenchidos até o momento do erro:")
        for field, value in result['form_data'].items():
            print(f"- {field}: {value}")