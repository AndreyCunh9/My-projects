import os
import pandas as pd

def receitas():
    # Diretório contendo os arquivos CSV
    diretorio = r"C:\Users\andrey.cunha\Downloads\Receita"

    # Lista para armazenar todos os DataFrames
    todos_dataframes = []

    # Loop através de todos os arquivos no diretório
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.csv'):
            # Lê o arquivo CSV e o adiciona à lista de DataFrames
            caminho_arquivo = os.path.join(diretorio, arquivo)
            print(f'Lendo arquivo: {caminho_arquivo}')
            df = pd.read_csv(caminho_arquivo)
            todos_dataframes.append(df)

    # Combina todos os DataFrames em um único DataFrame
    df_final = pd.concat(todos_dataframes, ignore_index=True)

    # Obtém o diretório do primeiro arquivo CSV encontrado
    diretorio_arquivo_csv = os.path.dirname(os.path.abspath(caminho_arquivo))

    arquivo_saida = os.path.join(diretorio_arquivo_csv, 'Receita_completa.csv')

    # Salva o DataFrame final como um arquivo CSV
    df_final.to_csv(arquivo_saida, index=False)

    print(f'Arquivo combinado salvo em: {arquivo_saida}')
