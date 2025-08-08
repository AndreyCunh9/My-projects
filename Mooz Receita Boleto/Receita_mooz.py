import os
import pandas as pd
from Protheus import mapeamento_codigo_vd
from Receita_comp import receitas
import time
import pandas as pd
from lxml import html
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from aguardar_download import aguardar_download
import tkinter as tk
from tkinter import simpledialog
import os
import shutil
from datetime import datetime
import re
from Mooz_boleto import Extrair_boletos
from urllib.parse import quote

Extrair_boletos()

receitas()

# Passo 1: Ler o arquivo CSV
caminho_csv = r"C:\Users\livia.maria\Downloads\Receita\Receita_completa.csv"
df = pd.read_csv(caminho_csv, delimiter=',')

# Passo 2: Separar a quinta coluna
coluna_filial = df.columns[5]
df_separado = df[coluna_filial].str.split('-', expand=True)

# Adicionar essas novas colunas de volta ao DataFrame original
df = df.drop(columns=[coluna_filial])
df_separado.columns = [f"{coluna_filial}_{i + 1}" for i in df_separado.columns]

# Inserir as novas colunas separadas na primeira posição
df = pd.concat([df_separado, df], axis=1)

# Passo 4: Mover a segunda coluna para a terceira posição
colunas = df.columns.tolist()
coluna_prefixo = colunas.pop(3)
coluna_tipo = colunas.pop(4)

colunas.insert(2, coluna_prefixo)
colunas.insert(4, coluna_tipo)
df = df[colunas]

# Passo 5: Apagar o conteúdo da nova segunda coluna e renomeá-la para "PREFIXO"
coluna_prefixo = df.columns[1]
df.rename(columns={coluna_prefixo: "PREFIXO"}, inplace=True)
df["PREFIXO"] = ""

# Renomear a coluna 4 para 'TIPO'
df = df.rename(columns={df.columns[3]: "TIPO"})

coluna_filial = df.columns[0]
df.rename(columns={coluna_filial: "FILIAL"}, inplace=True)

df['TIPO'] = 'BOL'

df = df.rename(columns={'Parcela': 'PARCELA'})
# Substituir sufixo ".0" por vazio e formatar para dois dígitos com zero à esquerda
df["PARCELA"] = df["PARCELA"].astype(str).str.replace(r"\.0$", "", regex=True).str.zfill(2)

df['Numero Pedido'] = df['Nr Nota Fiscal']
df = df.rename(columns={'Numero Pedido': 'TITULO'})
df["TITULO"] = df["TITULO"].astype(str).str.zfill(9)

#Passo 2: Salvar os valores da coluna 15
coluna_13 = df.iloc[:, 14]
coluna_12 = df.iloc[:, 10]

# Passo 3: Remover a coluna 15 do DataFrame
df = df.drop(columns=[df.columns[14]])
df = df.drop(columns=[df.columns[10]])

# Passo 4: Inserir os valores da coluna 15 como a sexta coluna do DataFrame
df.insert(5, "DATA_BAIXA", coluna_13)
df.insert(6, "VALOR", coluna_12)
df.insert(5, "BANCO", "")
df["BANCO"] = 'B03'
df.insert(6, "AGENCIA", "")
df["AGENCIA"] = '4494'
df.insert(7, "CONTA", "")
df["CONTA"] = '4494'
df["PREFIXO"] = "001"
# Passo 1: Verifique se os valores são strings e remova os pontos
df["VALOR"] = df["VALOR"].astype(str).str.replace(".", "", regex=False)

# Passo 2: Substitua as vírgulas por pontos
df["VALOR"] = df["VALOR"].str.replace(",", ".", regex=False)

# Passo 3: Filtre os valores negativos (se necessário)
df = df[~df["VALOR"].str.startswith('-')]

# Passo 4: Converta a coluna para float
df["VALOR"] = df["VALOR"].astype(float)

df["VALOR"] = df["VALOR"] * (1 - 0.0657)

# Passo 5: Arredondar para 2 casas decimais
df["VALOR"] = df["VALOR"].round(2)

# Remover linhas com valores vazios na coluna "VALOR"
df = df.dropna(subset=["VALOR"])

# Remover linhas com valores vazios na coluna "VALOR"
df = df.dropna(subset=["PARCELA"])

# Convertendo os valores de volta para strings
df["VALOR"] = df["VALOR"].astype(str)

# Substituindo os pontos por vírgulas
df["VALOR"] = df["VALOR"].str.replace(".", ",", regex=False, )

df["FILIAL"] = df["FILIAL"].str.strip().map(mapeamento_codigo_vd)

# Selecionar apenas as 10 primeiras colunas
df_10_colunas = df.iloc[:, :10]
print(df.iloc[:, :10])

user_dir = os.path.expanduser('~')
downloads_dir = os.path.join(user_dir, 'Downloads')

caminho_csv = os.path.join(downloads_dir, 'Importar_receita.csv')

# Salvar como arquivo CSV
df_10_colunas.to_csv(caminho_csv, sep=';', index=False)
