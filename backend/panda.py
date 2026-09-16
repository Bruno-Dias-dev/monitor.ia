import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv(override=True)

print("HOST:", os.environ.get("DB_HOST2"))
print("PORT:", os.environ.get("DB_PORT2"))
print("USER:", os.environ.get("DB_USER22"))
print("DATABASE:", os.environ.get("DB_NAME2"))
print("Password:", os.environ.get("DB_PASSWORD2"))

try:

    conexao = mysql.connector.connect(
        host=os.environ["DB_HOST2"],
        port=int(os.environ["DB_PORT2"]),
        user=os.environ["DB_USER22"],
        password=os.environ["DB_PASSWORD2"],
        database=os.environ["DB_NAME2"]
    )

    print("✅ Conectou!")
    print("Banco:", conexao.database)

    conexao.close()

except Exception as erro:

    print("❌ Erro:")
    print(erro)