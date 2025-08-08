import pandas as pd 
import glob
import os

caminho_arquivos = r"C:\Users\Ari Nascimento\Downloads\ARQUIVO EXCEL"

arquivo_xls = glob.glob(os.path.join(caminho_arquivos, '*xls'))

lista_dataframes =[]

for arquivo in arquivo_xls:
    df = pd.read_excel(arquivo)
    df_filtrado = df.dropna(subset=['Tipo Operação'])
    lista_dataframes.append(df_filtrado)

df_combined = pd.concat(lista_dataframes, ignore_index= True)

caminho_arquivo_final = r"T:\CONTAS A RECEBER\EEXTRATO"

df_combined.to_excel(caminho_arquivo_final, index= False)
