import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Carrega o .env
load_dotenv()

# Pega a URL do Excel
url = os.getenv("EXCEL_URL")

print("=" * 50)
print("TESTE DE DOWNLOAD DO EXCEL")
print("=" * 50)

print("\nURL encontrada:")
print(url)

# Faz o download
response = requests.get(url)

print("\nStatus:", response.status_code)
print("Content-Type:", response.headers.get("Content-Type"))
print("Tamanho:", len(response.content), "bytes")

# Verifica se a requisição deu erro
response.raise_for_status()

# Salva o arquivo
with open("teste.xlsx", "wb") as arquivo:
    arquivo.write(response.content)

print("\nExcel baixado com sucesso!")
print("Arquivo salvo como: teste.xlsx")

# ==========================
# TESTE DO PANDAS
# ==========================

print("\n" + "=" * 50)
print("TESTE DO PANDAS")
print("=" * 50)

# Lê o Excel
df = pd.read_excel("teste.xlsx")

print("\nPrimeiras linhas da planilha principal:")
print(df.head())

# Mostra as abas existentes
abas = pd.ExcelFile("teste.xlsx").sheet_names

print("\nAbas disponíveis:")
print(abas)

# ==========================
# TESTE DA ABA MEDIA
# ==========================

print("\n" + "=" * 50)
print("TESTE DA ABA 'media'")
print("=" * 50)

df_avaliacoes = pd.read_excel(
    "teste.xlsx",
    sheet_name="media"
)

print("\nPrimeiras linhas da aba media:")
print(df_avaliacoes.head())

print("\nColunas encontradas:")
print(df_avaliacoes.columns.tolist())

print("\nQuantidade de linhas:")
print(len(df_avaliacoes))

print("\nTESTE CONCLUÍDO!")