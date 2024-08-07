from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

from utils import pesquisar_trabalhador,marcando_exames

# acessando site
    
link = "https://portaldocliente.sfiec.org.br/login"
nav = webdriver.Chrome()
nav.maximize_window()
nav.get(link)

# login e senha

login=nav.find_element(By.XPATH, "//input[@name='login'][@type='text']")
login.send_keys('35669454391')

senha=nav.find_element(By.XPATH, "//input[@name='senha'][@type='password']")
senha.send_keys('cem@1570')
senha.submit()

# escolhendo a empresa

empresa=nav.find_element(By.CLASS_NAME, 'name')
empresa.click()
empresa.submit()

# Verificando se existe modal

time.sleep(10)

modal = None

try:
    modal = nav.find_element(By.ID, 'modal-generico')
except NoSuchElementException:
    modal = None

if modal:
    try:
        modal_close = modal.find_element(By.CLASS_NAME, 'close')
        modal_close.click()
    except NoSuchElementException:
        pass  # Lidar com a ausência do botão de fechamento, se necessário

original_window = nav.current_window_handle

link_autorizacao_agendamento = WebDriverWait(nav, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[@class='health-seso-system__link']/img[@src='https://portaldocliente.sfiec.org.br/style/imagens/sesi-system-link.png']"))
    )
link_autorizacao_agendamento.click()

# Esperar até que a nova aba seja aberta
WebDriverWait(nav, 10).until(EC.new_window_is_opened)

# Mudar para a nova aba
new_window = [window for window in nav.window_handles if window != original_window][0]
nav.switch_to.window(new_window)

time.sleep(3)

# Clicando em agendar "Nova"
iframe = WebDriverWait(nav, 10).until(
    EC.presence_of_element_located((By.ID, "iframe_menu"))
    )
# Mudar o contexto para o iframe
nav.switch_to.frame(iframe)

nova = WebDriverWait(nav, 10).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/a[3]/div"))
    )
nova.click()

#Clicando em "Incluir Trabalhadores"

incluir_trabalhadores = WebDriverWait(nav, 90).until(
    EC.element_to_be_clickable((By.ID, "sc_bt_inc_mult_trab_top"))
    )
incluir_trabalhadores.click()

nomes_trabalhadores = ['Abdias', 'Luan ARAUJO SOARES']

for nome in nomes_trabalhadores:
    situacao_cadastro = pesquisar_trabalhador(nav, nome)
    if situacao_cadastro == 'Incompleto':
        print(f"Situação cadastral incompleta para {nome}")
        # Guardar na planilha (implementação necessária)
    else:
        print(f"Situação cadastral de {nome} é {situacao_cadastro}")
        marcando_exames(nav)
        # Se encontrou um trabalhador com situação cadastral não "Incompleta", interrompe a busca
        break

    
