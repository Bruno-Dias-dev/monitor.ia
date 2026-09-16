"""Funções de acesso direto ao MySQL."""

import os
import mysql.connector
from mysql.connector import Error


def abrir_conexao():
    """Abre uma conexão nova somente quando uma rota precisa consultar o banco."""
    try:
        return mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", os.getenv("DB_HOST2")),
            port=int(os.environ["DB_PORT2"]),
            user=os.getenv("MYSQL_USER", os.getenv("DB_USER22")),
            password=os.getenv("MYSQL_PASSWORD", os.getenv("DB_PASSWORD2")),
            database=os.getenv("MYSQL_DATABASE", os.getenv("DB_NAME2")),
        )
    except Error:
        # A rota registra o erro técnico; não exponha dados da conexão aqui.
        raise
