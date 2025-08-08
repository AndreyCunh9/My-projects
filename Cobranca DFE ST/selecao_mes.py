import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime


# Função para selecionar o mês desejado no calendário
def selecionar_mes(driver):
    # Obter o mês atual
    mes_atual = datetime.now().month

    # Calcular o div correspondente ao mês desejado
    div_mes = mes_atual - 1 

    # Se o resultado for negativo, ajustar para lidar com o loop dos meses
    if div_mes <= 0:
        div_mes += 12

    # XPaths para o botão do calendário e para o mês específico
    xpath_botao_calendario = '//*[@id="pickerForm"]/jhi-new-month-date-picker/div/div[1]/div/button'
    xpath_mes_desejado = f'//*[@id="pickerForm"]/jhi-new-month-date-picker/div/div[2]/div/div[{div_mes}]'

    # Clicar no botão do calendário
    calendario_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath_botao_calendario))

    )

    # Esperar até que a sobreposição desapareça
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".black-overlay")))

    calendario_button.click()

    time.sleep(4)

    # Esperar e clicar no mês desejado
    mes_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath_mes_desejado))
    )
    mes_button.click()


    time.sleep(2)

    # Clicar no botao para selecionar em aberto, liquidado ou todos
    botao_selecione_sit = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                                    '// *[@ id="situacoesForm"] / ng-select'))
    )
    botao_selecione_sit.click()

    #Clicar em todos
    botao_sit_todos = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/jhi-main/div[2]/div/jhi-calculo-nfe/div/jhi-filtros-pesquisa/form/div/fieldset/div/div/div[4]/jhi-select-situacoes/form/ng-select/ng-dropdown-panel/div/div[2]/div[6]'))
    )
    botao_sit_todos.click()
    time.sleep(2)

    # Encontrar e clicar no botão específico após selecionar o mês
    botao_calculo_nfe = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                                    '/html/body/jhi-main/div[2]/div/jhi-calculo-nfe/div/jhi-filtros-pesquisa/form/div/div/div[2]/button'))
    )
    botao_calculo_nfe.click()
    time.sleep(3)

    botao_st = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                                    '//*[@id="3"]'))
    )
    botao_st.click()
    time.sleep(3)
