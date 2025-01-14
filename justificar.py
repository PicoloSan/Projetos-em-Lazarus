# Importando bibliotecas do Excel, do Chrome e do Selenium
import ctypes
import openpyxl                                                   # type: ignore
from selenium import webdriver                                    # type: ignore
from selenium.webdriver.common.by import By                       # type: ignore
from selenium.webdriver.support.ui import Select                  # type: ignore
from selenium.webdriver.support.ui import WebDriverWait           # type: ignore
from selenium.webdriver.support import expected_conditions as EC  # type: ignore
import time
import json

# Função para alterar a prioridade
def set_process_priority(priority_class):
    # Obtém o identificador do processo atual
    process_handle = ctypes.windll.kernel32.GetCurrentProcess()
    # Altera a prioridade do processo
    ctypes.windll.kernel32.SetPriorityClass(process_handle, priority_class)

# Prioridades disponíveis
IDLE_PRIORITY_CLASS = 0x00000040
BELOW_NORMAL_PRIORITY_CLASS = 0x00004000
NORMAL_PRIORITY_CLASS = 0x00000020
ABOVE_NORMAL_PRIORITY_CLASS = 0x00040000
HIGH_PRIORITY_CLASS = 0x00000080
REALTIME_PRIORITY_CLASS = 0x00000100

# função escreve no arquivo
def write_log(texto, caminho_arquivo):
    # Abra o arquivo em modo de append
    with open(caminho_arquivo, 'a') as file:
        file.write(texto + '\n')

# função lê arquivo json
"""
usr    = usuário do Sismed
pwd    = senha do Sismed
file   = pasta de trabalho do excel
sheet  = planilha
log    = arquivo de log
column = coluna da planilha que contém as Ordens de Serviço
"""
def read_json(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        dados = json.load(arquivo)
        return dados

# Defina a prioridade desejada, por exemplo, abaixo do normal
set_process_priority(BELOW_NORMAL_PRIORITY_CLASS)

# lê os arquivos de configuração do json
dados = read_json('justificar.json')

# define o arquivo de log como justificar.log
arquivolog = dados['log']

# Carrega o arquivo Excel
umlog = 'Carregando informações...'
write_log(umlog, arquivolog)

# escreve qual arquivo do excel está abrindo no log
umarquivo = dados['file']
umlog = 'Lendo planilha: "' + str(umarquivo) + '" ...'
write_log(umlog, arquivolog)

# abre a planilha da pasta de trabalho do excel
umaplanilha = dados['sheet']
workbook = openpyxl.load_workbook(umarquivo)
sheet = workbook[umaplanilha]
# sheet = workbook.active

# Obter os valores da coluna 'D'
umacoluna = dados['column']
umlog = 'Lendo a coluna ' + str(umacoluna) + ' da planilha ' + str(umaplanilha) + ' ...'
write_log(umlog, arquivolog)
column_values = [cell.value for cell in sheet[umacoluna] if cell.value is not None]

# Inicializar o driver do Chrome
driver = webdriver.Chrome()

# Define o tempo limite para 30 segundos
driver.implicitly_wait(30)

# Navegar até a página desejada
URLlogin = dados['URLlogin']
driver.get(URLlogin)
login_txt = driver.find_element(By.ID, "formLoginExterno:itUsuario")
usuario = dados['usr']
driver.execute_script("arguments[0].value = arguments[1];", login_txt, usuario)
passw_txt = driver.find_element(By.NAME, "formLoginExterno:j_id41")
senha = dados['pwd']
driver.execute_script("arguments[0].value = arguments[1];", passw_txt, senha)
submit_button = driver.find_element(By.NAME, "formLoginExterno:j_id43")
submit_button.click()

# Captura a URL das Ordens de Serviço
URLos = dados['URLos']

# Preencher os campos e executar a macro
index = 0
while index < len(column_values):
    value = column_values[index]

    try:
        # Escreve o valor que parou se parou
        umlog = 'A OS atual é: ' + str(value) + '.'
        write_log(umlog, arquivolog)

        driver.get(URLos)

        # Encontrar o campo e preencher com o valor
        field = driver.find_element(By.ID, "formOrdemServicoList:itCodOrdemServico")
        driver.execute_script("arguments[0].value = arguments[1];", field, value)

        enviar_button = driver.find_element(By.ID, "formOrdemServicoList:clDetalharOrdemServico")
        enviar_button.click()

        # Espere 3 segundos para executar o javascript de fechar  o modal
        time.sleep(3)
        
        # Fecha o popup executando o javascript de fechar modal, do 'X' do canto do modal
        # driver.execute_script("closeModalPanel();")
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div/div[2]/div/img")))
        export_button = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[2]/div/img")
        export_button.click()

        # Espere 3 segundos antes de fechar o navegador
        time.sleep(3)
       
        # Encontre o elemento <select>
        select_element = driver.find_element(By.NAME, "j_id184:j_id223")

        # Crie um objeto Select a partir do elemento
        select = Select(select_element)

        # Selecione a opção pelo valor
        select.select_by_value("5")
        # ORDEM DE SERVIÇO PROGRAMADA COM ATRASO

        # Ou selecione a opção pelo texto visível
        # select.select_by_visible_text("Option Text")
        
        textarea_txt = driver.find_element(By.NAME, "j_id184:j_id262")
        driver.execute_script("arguments[0].value = arguments[1];", textarea_txt, "OS programada em atraso")
        # Motivo anterior:
        # Devido o atendimento a Diretoria da Copasa, priorizamos os serviços de Substituição de Hidrômetros PMQM e os serviços de Confirmação de Infração.

        # Espere 3 segundos para clicar em salvar no popup
        time.sleep(3)
        
        salvar_button = driver.find_element(By.ID, "j_id184:j_id280")
        salvar_button.click()

        # Espere 3 segundos para clicar em salvar no rodapé
        time.sleep(3)
        
        salvar2_button = driver.find_element(By.ID, "formOrdemServico:cbGravar")
        salvar2_button.click()

        # Espere 3 segundos para executar o próximo registro ou fechar o navegador
        time.sleep(3)

        index += 1
        
    except Exception as e:
        umlog = 'Erro ao processar o código ' + str(value) + ': ' + str(e) + ' ' 
        write_log(umlog, arquivolog)
        umlog = 'Tentando novamente...'
        write_log(umlog, arquivolog)


umlog = 'Concluído com sucesso!'
write_log(umlog, arquivolog)

# Fechar o navegador
driver.quit()