
import os
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

host = os.environ["DB_HOST2"]
user = os.environ["DB_USER2"]
password = os.environ["DB_PASSWORD2"]
database = os.environ["DB_NAME2"]

try:
    conexao = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    if conexao.is_connected():
        print("✅ Conexão com o banco realizada com sucesso!")

        cursor = conexao.cursor()
        cursor.execute("SELECT 1")

        resultado = cursor.fetchone()
        print(f"✅ Teste de consulta: {resultado}")

        cursor.close()
        conexao.close()

except mysql.connector.Error as erro:
    print("❌ Erro ao conectar ao banco:")
    print(erro)
