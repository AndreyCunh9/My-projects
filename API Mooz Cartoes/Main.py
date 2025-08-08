import json
import os
import requests
from requests.auth import HTTPBasicAuth
from Lojas_varejo import mapeamento_cod_filial
from Extrair_pagamentos import extrato_pag
from Extrair_vendas import extrair_relat_vendas
from Portal_EEXTRATO import Importar_arquivo
import time
from datetime import datetime, timedelta
from Main_practico import extrair_practico
import shutil
import pyautogui
import pandas as pd

extrato_pag()

extrair_relat_vendas()

extrair_practico()

Importar_arquivo()
