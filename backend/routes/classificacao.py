import os 
import mysql.connector
from flask import jsonify, Blueprint
from login import conectar_db
from pathlib import Path
from dotenv import load_dotenv
from registro import conectar_db_avaliacoes
from datetime import date


raiz_projeto = Path(__file__).resolve().parents[2]
load_dotenv(raiz_projeto / ".env")

conexao = conectar_db_avaliacoes()

cursor = conexao.cursor()
cursor.execute("""
    SELECT 
        contemplado,
        ROUND(AVG(saudacao), 2) AS media_saudacao,
        ROUND(AVG(clareza), 2) AS media_clareza,
        ROUND(AVG(conhecimento), 2) AS media_conhecimento,
        ROUND(AVG(resolucao), 2) AS media_resolucao,
        ROUND(AVG(empatia), 2) AS media_empatia
    FROM avaliacao_atendimentos
    WHERE criado_em >= '2026-01-01'
        AND criado_em < '2027-01-01'
        AND contemplado IS NOT NULL
    GROUP BY contemplado;
""")

hoje = date.today().strftime("%Y-%m-%d")

resultados = cursor.fetchall()

print(resultados)

cursor.close()
conexao.close()