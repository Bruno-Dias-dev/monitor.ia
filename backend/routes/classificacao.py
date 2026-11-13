import os 
import mysql.connector
from flask import jsonify, Blueprint, request
from routes.login import conectar_db
from pathlib import Path
from dotenv import load_dotenv
from routes.registro import conectar_db_avaliacoes
from datetime import date, timedelta

raiz_projeto = Path(__file__).resolve().parents[2]
load_dotenv(raiz_projeto / ".env")

classificacao_bp = Blueprint("classificacao", __name__)

@classificacao_bp.route("/api/classificacao", methods=["GET"])
def classificacao():


    dataInicial = request.args.get("data_inicial")
    dataFinal = request.args.get("data_final")

    print(dataInicial, dataFinal)

    # Captura das datas
    if not dataInicial and not dataFinal:

        # Calculo do range da semana atual
        hoje = date.today()
        inicio_semana = hoje - timedelta(days=hoje.weekday())
        fim_semana = inicio_semana + timedelta(days=7)
        

        try:
            conexao = conectar_db_avaliacoes()

            cursor = conexao.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    contemplado,
                    ROUND(AVG(saudacao), 2) AS media_saudacao,
                    ROUND(AVG(clareza), 2) AS media_clareza,
                    ROUND(AVG(conhecimento), 2) AS media_conhecimento,
                    ROUND(AVG(resolucao), 2) AS media_resolucao,
                    ROUND(AVG(empatia), 2) AS media_empatia
                FROM avaliacao_atendimentos
                WHERE criado_em >= %s
                    AND criado_em < %s
                    AND contemplado IS NOT NULL
                GROUP BY contemplado;
            """, (inicio_semana, fim_semana))

            registros = cursor.fetchall()

            cursor.close()

            conexao.close()

            return jsonify({
                "sucesso": True,
                "registro": registros
            }), 200

        except Exception as erro:
            print(f"Erro ao consultar avaliações: {erro}")

            return jsonify({
                "error": f"Erro ao consultar banco de dados",
                "mensagem": str(erro)
            }), 500

    else: 

        try:
                conexao = conectar_db_avaliacoes()
        
                cursor = conexao.cursor(dictionary=True)
                cursor.execute("""
                    SELECT 
                        contemplado,
                        ROUND(AVG(saudacao), 2) AS media_saudacao,
                        ROUND(AVG(clareza), 2) AS media_clareza,
                        ROUND(AVG(conhecimento), 2) AS media_conhecimento,
                        ROUND(AVG(resolucao), 2) AS media_resolucao,
                        ROUND(AVG(empatia), 2) AS media_empatia
                    FROM avaliacao_atendimentos
                    WHERE criado_em >= %s
                        AND criado_em < %s
                        AND contemplado IS NOT NULL
                    GROUP BY contemplado;
                """, (dataInicial, dataFinal))
        
                registros = cursor.fetchall()
        
                cursor.close()
        
                conexao.close()

                print(registros)
        
                return jsonify({
                    "sucesso": True,
                    "registro": registros
                }), 200
        
        except Exception as erro:
            print(f"Erro ao consultar avaliações: {erro}")
        
            return jsonify({
                "error": f"Erro ao consultar banco de dados",
                "mensagem": str(erro)
            }), 500