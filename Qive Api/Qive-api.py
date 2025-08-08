import requests

url = "https://api.arquivei.com.br/v1/nfe/received"
headers = {
    "X-API-ID": "3e51eeaeb4c678bb648801cbc545da9cc75682cf",
    "X-API-KEY": "73d6941b0c948ac010b35c4f57506072dac44a4f",
    "Content-Type": "application/json"
}

# Parâmetros iniciais
params_base = {
    "created_at[from]": "2025-06-01",
    "created_at[to]": "2025-06-17",
    "format_type": "JSON",
    "limit": 50  # máximo permitido pela API
}

# Início da paginação
cursor = 0
total_documentos = 0

while True:
    # Copia os params base e adiciona o cursor atual
    params = params_base.copy()
    params["cursor"] = cursor

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Erro: {response.status_code} - {response.text}")
        break

    data = response.json()
    documentos = data.get("data", [])

    print(f"🔄 Página com {len(documentos)} documentos recebidos (cursor {cursor})")
    total_documentos += len(documentos)

    # Pegando o próximo cursor da resposta
    next_cursor = data.get("cursor", {}).get("next")

    if not next_cursor or len(documentos) == 0:
        break  # Terminou a paginação

    cursor = next_cursor  # Avança para a próxima página

print(f"✅ Total de documentos coletados: {total_documentos}")
