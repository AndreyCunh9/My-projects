import json
import requests
from requests.auth import HTTPBasicAuth
import os
from datetime import datetime, timedelta
import time


def extrair_relat_vendas():
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

    def salvar_em_txt(conteudo, nome_arquivo, pasta_destino):
        """
        Salva o conteúdo em um arquivo de texto.

        Args:
            conteudo (str): Conteúdo a ser salvo.
            nome_arquivo (str): Nome do arquivo onde o conteúdo será salvo.
            pasta_destino (str): Caminho do diretório onde o arquivo será salvo.
        """
        caminho_completo = os.path.join(pasta_destino, nome_arquivo)
        with open(caminho_completo, 'w') as arquivo:
            arquivo.write(conteudo)

    pasta_destino = r"T:\CONTAS A RECEBER\EEXTRATO"

    # Exemplo de uso da função
    tipo = "VENDA"

    data = (datetime.now() - timedelta(1)).strftime("%d%m%Y")
    print(data)
    codigo = '4494'
    usuario = "10269.api"  # Substitua com seu nome de usuário
    senha = "YCYUb4BK"  # Substitua com sua senha
    extrato = get_extrato(tipo, data, codigo, usuario, senha)

    # Verificar se o retorno é um dicionário ou uma mensagem de erro
    if isinstance(extrato, dict):
        conteudo_txt = json.dumps(extrato, indent=4)
    else:
        conteudo_txt = extrato

    # Nome do arquivo baseado no código da filial
    nome_arquivo = f"Vendas{data}{codigo}.txt"
    salvar_em_txt(conteudo_txt, nome_arquivo, pasta_destino)
    print(f"Extrato salvo em {os.path.join(pasta_destino, nome_arquivo)}")
