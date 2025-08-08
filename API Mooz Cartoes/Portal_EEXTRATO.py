from datetime import datetime, timedelta
import time
import pyautogui
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def obter_data_ultimo_dia_util():
    hoje = datetime.now()
    if hoje.weekday() == 0:  # Segunda-feira
        ultimo_dia_util = hoje - timedelta(days=3)
    elif hoje.weekday() == 6:  # Domingo
        ultimo_dia_util = hoje - timedelta(days=2)
    else:
        ultimo_dia_util = hoje - timedelta(days=1)
    return ultimo_dia_util.strftime("%d%m%Y")


def executar_script():
    hoje = datetime.now()
    if hoje.weekday() >= 5:  # Sábado (5) ou Domingo (6)
        print("Hoje não é um dia útil. O script será executado apenas de segunda a sexta-feira.")
        return

    data_ultimo_dia_util = obter_data_ultimo_dia_util()
    print(f"Último dia útil: {data_ultimo_dia_util}")

    try:
        url = 'https://www.eextrato.com.br/conciliador/pages/integracao/uploadArquivoHagana.xhtml'
        driver = webdriver.Edge()
        driver.get(url)
        driver.maximize_window()
        time.sleep(2)

        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="user"]'))
        )
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="password"]'))
        )

        username_field.send_keys("LIVIA.MARIA")
        password_field.send_keys("Extrato235711#")

        entrar_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="entrar"]'))
        )
        entrar_button.click()
        time.sleep(5)

        vendas_localizacao = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div[1]/form/header/div/div/div[4]/ul/li[1]/a/span'))
        )
        vendas_localizacao.click()

        arquivo_hagana = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="form:j_idt109"]/ul[2]/li/ul/li[6]/a'))
        )
        arquivo_hagana.click()
        time.sleep(2)

        upload_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            '/html/body/div[1]/div[2]/div[1]/div[1]/form[3]/div/div/div/span/div['
                                            '1]/span/div/div/div[1]/span'))
        )
        upload_element.click()
        time.sleep(2)
        for i in range(6):
            pyautogui.press("tab", interval=0.5)
        pyautogui.press("enter")

        pyautogui.write("T:\\CONTAS A RECEBER\\EEXTRATO", interval=0.5)
        pyautogui.press("enter")

        for i in range(6):
            pyautogui.press("tab", interval=0.5)
        pyautogui.press("enter")
        pyautogui.write(f"Extrato_pagamentos{data_ultimo_dia_util}.txt", interval=0.7)
        pyautogui.press("enter")

        time.sleep(5)
        upload_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            '/html/body/div[1]/div[2]/div[1]/div[1]/form[3]/div/div/div/span/div[1]/span/div/div/div[1]/span'))
        )
        upload_element.click()
        time.sleep(5)

        pyautogui.write(f"vendas{data_ultimo_dia_util}4494.txt", interval=0.7)
        pyautogui.press("enter")

        time.sleep(5)

        vendas_localizacao = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div[1]/form/header/div/div/div[4]/ul/li[1]/a/span'))
        )
        vendas_localizacao.click()

        arquivo_practico = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="form:j_idt109"]/ul[2]/li/ul/li[8]/a'))
        )
        arquivo_practico.click()
        time.sleep(5)

        arquivo_practico_upload = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[1]/form['
                                                  '3]/div/div/div/span/div[1]/span/div/div/div[1]/span'))
        )
        arquivo_practico_upload.click()

        time.sleep(5)

        pyautogui.write(f"arquivo_agrupado.xlsx", interval=0.7)
        time.sleep(5)
        pyautogui.press("enter")
        time.sleep(5)


    except TimeoutException:
        print("Tempo limite excedido ao tentar encontrar elementos na página.")
    finally:
        driver.quit()


def Importar_arquivo():
    executar_script()


if __name__ == "__main__":
    Importar_arquivo()
