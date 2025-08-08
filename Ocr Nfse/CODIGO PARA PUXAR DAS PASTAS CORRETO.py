import os
from pdfminer.high_level import extract_text

# Função para extrair o texto de um arquivo PDF
def extract_text_from_pdf(pdf_path):
    text = extract_text(pdf_path)
    return text

# Pasta contendo os arquivos PDF
folder_path = r"C:\Users\andrey.cunha\Downloads\ND"
# Percorrer todos os arquivos na pasta
for filename in os.listdir(folder_path):
    # Verificar se o arquivo é um PDF
    if filename.endswith(".pdf"):
        # Caminho completo para o arquivo PDF
        pdf_path = os.path.join(folder_path, filename)
        
        # Extrair texto do arquivo PDF
        text = extract_text_from_pdf(pdf_path)
        
        # Imprimir o nome do arquivo e o texto extraído
        print("Arquivo:", filename)
        print("Texto extraído:", text)
        print()
