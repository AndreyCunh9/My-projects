import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selecao_mes import selecionar_mes
import pandas as pd
from Credentiais import credenciais
from extracao_dados import extrair_dados
from ret_creds import cred

# URL da página inicial
url = 'https://contribuinte.sefaz.al.gov.br/cobrancadfe/#/'

extrair_dados

if __name__ == "__main__":
    cred()
