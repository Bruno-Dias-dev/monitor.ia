from flask import request, jsonify
import mysql.connector
import os

@app.route("/api/avaliacoes", methods=["GET"])
def buscar_avaliacoes():

    data_inicial = request.args.get("data_inicial")
    data_final = request.args.get("data_final")

    if not data_inicial or not data_final:
        return jsonify({
            "sucesso": False,
            "error": "VALIDACAO",
            "mensagem": "Informe a data inicial e a data final."
        }), 400

    try:
        conexao = mysql.connector.connect(
            host=os.environ["DB_HOST2"],
            user=os.environ["DB_USER2"],
            password=os.environ["DB_PASSWORD2"],
            database=os.environ["DB_NAME2"]
        )

        cursor = conexao.cursor(dictionary=True)

        sql = """
            SELECT
                id,
                identificador_unico,
                data,
                canal,
                contemplado,
                beneficiario,
                numero,
                saudacao,
                clareza,
                conhecimento,
                resolucao,
                empatia,
                score_qualidade,
                risco_processo,
                resolvido,
                reincidencia,
                observacoes,
                acao_gerencial,
                criado_em,
                conversacao
            FROM avaliacao_atendimentos
            WHERE data >= %s
              AND data < DATE_ADD(%s, INTERVAL 1 DAY)
            ORDER BY data DESC
        """

        cursor.execute(sql, (data_inicial, data_final))

        registros = cursor.fetchall()

        cursor.close()
        conexao.close()

        return jsonify({
            "sucesso": True,
            "registros": registros
        }), 200

    except Exception as erro:
        print(f"Erro ao consultar avaliações: {erro}")

        return jsonify({
            "error": "Erro ao consultar avaliações no banco.",
            "mensagem": str(erro)
        }), 500
