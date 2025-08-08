import json
import os
import time
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
from Lojas_varejo import mapeamento_cod_filial


def extrato_pag():
    def get_extrato(tipo, data, codigo, usuario, senha):
        """
        Faz uma requisição GET à API de extratos com autenticação básica.

        Args:
            tipo (str): Tipo do extrato ("PAGAMENTO" ou "VENDA").
            data (str): Data de referência no formato "ddMMaaaa".
            codigo (str): Código da franquia.
            usuario (str): Nome de usuário para autenticação.
            senha (str): Senha para autenticação.

        Returns:
            dict/str: Retorna o extrato em formato JSON se sucesso, ou uma mensagem de erro.
        """
        base_url = "https://www.hagana-adquirencia.com.br/portal/extratos"
        parametros = {
            "tipo": tipo,
            "dataReferencia": data,
            "codigoFranquia": codigo
        }

        try:
            response = requests.get(base_url, params=parametros, auth=HTTPBasicAuth(usuario, senha))
            response.raise_for_status()

            # Tentar analisar a resposta como JSON
            try:
                return response.json()
            except ValueError:
                # Se a resposta não for um JSON válido, retornar o conteúdo da resposta
                return f"{response.text}"
        except requests.exceptions.HTTPError as http_err:
            return f"HTTP error occurred: {http_err}"
        except requests.exceptions.ConnectionError as conn_err:
            return f"Connection error occurred: {conn_err}"
        except requests.exceptions.Timeout as timeout_err:
            return f"Timeout error occurred: {timeout_err}"
        except requests.exceptions.RequestException as req_err:
            return f"An error occurred: {req_err}"


    def salvar_em_txt(conteudos, nome_arquivo, pasta_destino):
        """
        Salva o conteúdo em um arquivo de texto.

        Args:
            conteudo (str): Conteúdo a ser salvo.
            nome_arquivo (str): Nome do arquivo onde o conteúdo será salvo.
        """
        caminho_completo = os.path.join(pasta_destino, nome_arquivo)
        with open(caminho_completo, 'w') as arquivo:
            for conteudo in conteudos:
                arquivo.write(conteudo + "\n")

    # Função para obter a data do último dia útil
    def obter_data_ultimo_dia_util():
        hoje = datetime.now()
        # Se hoje for segunda-feira, o último dia útil é a última sexta-feira
        if hoje.weekday() == 0:
            ultimo_dia_util = hoje - timedelta(days=3)
        # Se hoje for domingo, o último dia útil é a última sexta-feira
        elif hoje.weekday() == 6:
            ultimo_dia_util = hoje - timedelta(days=2)
        # Caso contrário, subtrai um dia
        else:
            ultimo_dia_util = hoje - timedelta(days=1)
        return ultimo_dia_util.strftime("%d%m%Y")

    # Função principal para executar o script somente em dias úteis
    def executar_script():
        hoje = datetime.datetime.now()
        # Se hoje for sábado (5) ou domingo (6), não executa o script
        if hoje.weekday() >= 5:
            print("Hoje não é um dia útil. O script será executado apenas de segunda a sexta-feira.")
            return


    # Lista para armazenar todos os conteúdos dos extratos
    extratos_consolidados = []

    # Caminho da pasta onde os arquivos serão salvos
    pasta_destino = r"T:\CONTAS A RECEBER\EEXTRATO"

    # Exemplo de uso da função
    tipo = "PAGAMENTO"

    # Calcula a data do último dia útil
    data_ultimo_dia_util = obter_data_ultimo_dia_util()
    print(data_ultimo_dia_util)

    usuario = "10269.api"  # Substitua com seu nome de usuário
    senha = "YCYUb4BK"  # Substitua com sua senha

    for codigo in mapeamento_cod_filial:
        extrato = get_extrato(tipo, data_ultimo_dia_util, codigo, usuario, senha)

        # Verificar se o retorno é um dicionário ou uma mensagem de erro
        if isinstance(extrato, dict):
            conteudo_txt = json.dumps(extrato, indent=4)
        else:
            conteudo_txt = extrato

        extratos_consolidados.append(conteudo_txt)

    # Nome do arquivo para extratos consolidados
    nome_arquivo_consolidado = f"Extrato_pagamentos{data_ultimo_dia_util}.txt"
    salvar_em_txt(extratos_consolidados, nome_arquivo_consolidado, pasta_destino)
    print(f"Extratos consolidados salvos em {os.path.join(pasta_destino, nome_arquivo_consolidado)}")
    time.sleep(2)
