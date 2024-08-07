from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
import time

def pesquisar_trabalhador(nav, nome):
    try:
        # Clicando em "Pesquisa avançada"
        pesq_avancada = WebDriverWait(nav, 10).until(
            EC.element_to_be_clickable((By.ID, "pesq_top"))
        )
        pesq_avancada.click()

        # Clicando em nome
        nome_trabalhador = WebDriverWait(nav, 10).until(
            EC.element_to_be_clickable((By.ID, "SC_c_nome"))
        )
        nome_trabalhador.clear()
        nome_trabalhador.send_keys(nome)
        nome_trabalhador.submit()

        # Verificar a situação cadastral
        situacao_cadastro = WebDriverWait(nav, 10).until(
            EC.visibility_of_element_located((By.ID, 'id_sc_field_situacao_cadastro_1'))
        ).text

        return situacao_cadastro
    except TimeoutException:
        print(f"Timeout ao pesquisar o trabalhador: {nome}")
        return None

def marcando_exames(nav):
    try:
        print("Marcando operador")
        # Marcando operador
        checkbox = WebDriverWait(nav, 10).until(
            EC.element_to_be_clickable((By.ID, "NM_ck_run1"))
        )
        checkbox.click()
    except TimeoutException:
        print("Erro: Falha ao marcar operador")
        return

    try:
        print("Incluindo trabalhador")
        # Incluir trabalhador
        incluir_trabalhador = WebDriverWait(nav, 10).until(
            EC.element_to_be_clickable((By.ID, 'sc_incluir_trabalhador_top'))
        )
        incluir_trabalhador.click()
    except TimeoutException:
        print("Erro: Falha ao incluir trabalhador")
        return
    
    lista_exames=['Consulta Ocupacional - ASO Admissional TAP','Audiometria','Hemograma com Contagem de Plaquetas ou Frações (Eritrograma, Leucograma, Plaquetas)', 'Triagem Teste de Acuidade Visual']

    escolhendo_exames(nav, lista_exames)
    # autorizar(nav)

def escolhendo_exames(nav, lista_exames):
    
    for exame in lista_exames:
        
        try:
            print("Incluindo serviços")
            # Incluir serviços
            incluir_servicos = WebDriverWait(nav, 10).until(
                EC.element_to_be_clickable((By.ID,'sc_bt_inc_mult_serv_top'))
            )
            incluir_servicos.click()
        except TimeoutException:
            print("Erro: Falha ao incluir serviços")
            return
    
        try:
            print("Buscando serviço (primeiro clique)")
            # Buscar serviço (primeiro clique)
            btn_buscar_servico = WebDriverWait(nav, 10).until(
                EC.element_to_be_clickable((By.ID, 'pesq_top'))
            )
            btn_buscar_servico.click()
        except TimeoutException:
            print("Erro: Falha ao buscar serviço (primeiro clique)")
            return

        # Inputando nome do exame
        try:
            print("Inputando nome do exame")
            input_nome_exame = WebDriverWait(nav, 10).until(
                EC.element_to_be_clickable((By.ID, 'SC_s_nome'))
            )
            input_nome_exame.clear()
            input_nome_exame.send_keys(exame)
            print(f"Serviço {exame} adicionar com sucesso")
        except TimeoutException:
            print("Erro: Falha ao buscar exame")
            return

        # Botão de pesquisar exame
        try:
            print("Clicando em pesquisar exame")
            btn_pesquisar = WebDriverWait(nav, 10).until(
                EC.element_to_be_clickable((By.ID, 'sc_b_pesq_bot'))
            )
            btn_pesquisar.click()
        except TimeoutException:
            print("Erro: Falha ao clicar em pesquisar exame")
            return

        #verificandos e encontrou ou não o exame
        try:
            print('verificando se encontrou algum exame')
            verif_exame=WebDriverWait(nav, 10).until(
                EC.element_to_be_clickable((By.ID, 'sc_grid_body'))
                )
            if verif_exame.text == 'Registros não encontrados':
                print('Serviço não encontrado')
                return
            else:
                print('Exame encontrado!')
                pass
        except TimeoutException:
            print("Erro: falha ao verificar se o exame existe")
            return
        
        try:
            element = WebDriverWait(nav, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'css_toolbar_obj'))
            )
            
            # Obtenha o texto do elemento
            text = element.text

            # Se precisar extrair apenas a parte numérica, você pode fazer isso usando expressão regular
            import re
            match = re.search(r'de (\d+)', text)
            if match:
                extracted_number = int(match.group(1))
                if extracted_number > 1:
                    print('Lista de exames possui mais de 1 exame. O nome do exame precisa ser correto!')
                    return
                else:
                    print('A lista possui apenas 1 exame, seguir..')
                    pass
            else:
                print("Não foi possível extrair o valor numérico desejado.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            
        # marcando exame
        try:
            print("Marcando checkbox do exame escolhido")
            checkbox_exame=WebDriverWait(nav,10).until(
                EC.visibility_of_element_located((By.ID, 'NM_ck_run1'))
                )
            checkbox_exame.click()
        except TimeoutException:
            print("Erro: Falha ao clicar no checkbox do exame escolhido")
            return
        
        try:
            print("Voltando para tela de autorização")
            btn_buscar_servico = WebDriverWait(nav, 10).until(
                EC.element_to_be_clickable((By.ID, 'sc_incluir_servico_top'))
            )
            btn_buscar_servico.click()
        except TimeoutException:
            print("Erro: Falha ao voltar para tela de autorizacao")
            return
        
def autorizar(nav):
    
    try:
        print("Botão de autorizar")
        btn_autorizar = WebDriverWait(nav, 10).until(
            EC.element_to_be_clickable((By.ID, 'sc_bt_autorizar_top'))
        )
        btn_autorizar.click()
    except TimeoutException:
        print("Erro: Falha ao clicar no Botão de autorizar")
        return
    
    # caso tenha botão de alerta
    
    # Aguarde até que o alerta esteja presente
    WebDriverWait(nav, 10).until(EC.alert_is_present())

    # Mude para o alerta
    alert = nav.switch_to.alert

    # Obtenha o texto do alerta
    alert_text = alert.text
    print(f"O texto do alerta é: {alert_text}")
    
    # Aceite o alerta
    alert.accept()

    # Se quiser clicar no botão "Cancel" (se disponível)
    # alert.dismiss()
    
    #confirmando agendamento
    try:
        print("Confirmando agendamento")
        # Marcando operador
        checkbox = WebDriverWait(nav, 10).until(
            EC.element_to_be_clickable((By.ID, "sc_btn_sim_bot"))
        )
        checkbox.click()
    except TimeoutException:
        print("Erro: Falha ao confirmar agendamento")
        return
    
    #preenchendo data    
    try:
        print('Preenchendo data')
        # Aguarde até que o elemento <select> esteja presente e clicável
        select_element = WebDriverWait(nav, 10).until(
            EC.element_to_be_clickable((By.ID, 'id_sc_field_data'))
        )

        # Inicialize a classe Select com o elemento <select>
        select = Select(select_element)

        # Selecione a opção com o valor "1"
        select.select_by_value('1')

    except TimeoutException:
        print(f"Ocorreu um erro: ao selecionar a data.")
        return
    
    #preenchendo cidade
    try:
        print('Preenchendo cidade')
        # Aguarde até que o elemento <select> esteja presente e clicável
        select_element = WebDriverWait(nav, 10).until(
            EC.element_to_be_clickable((By.ID, 'id_sc_field_cidade'))
        )

        # Inicialize a classe Select com o elemento <select>
        select = Select(select_element)

        # Selecione a opção com o valor "1"
        select.select_by_value('2304400')

    except TimeoutException:
        print(f"Ocorreu um erro: ao selecionar a cidade")
        return
    
    time.sleep(2)
        
    #fechando mensagem de erro
    try:
        print('fechando mensagem de erro')
        # Aguarde até que o elemento <a> esteja presente e clicável
        fechar_link = WebDriverWait(nav, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[title="Fechar"]'))
        )

        # Clique no link
        fechar_link.click()

    except TimeoutException:
        print(f"Mensagem de erro não apareceu")
        pass

    #preenchendo local
    try:
        print('Preenchendo local')
        # Aguarde até que o elemento <select> esteja presente e clicável
        select_element = WebDriverWait(nav, 10).until(
            EC.element_to_be_clickable((By.ID, 'id_sc_field_local'))
        )

        # Inicialize a classe Select com o elemento <select>
        select = Select(select_element)

        # Selecione a opção com o valor "1"
        select.select_by_value('56')

    except TimeoutException:
        print(f"Ocorreu um erro: ao selecionar o local")
        return
        
    datainicial = WebDriverWait(nav,10).until(
        EC.element_to_be_clickable((By.ID, 'id_read_on_data_ini'))
        )
    datainicial=datainicial.text
    
    datafinal = WebDriverWait(nav,10).until(
        EC.element_to_be_clickable((By.ID, 'id_read_on_data_ini'))
        )
    datafinal=datafinal.text
    
    
    
    # confirmar novamente
    # confirmar no .alert
    # 