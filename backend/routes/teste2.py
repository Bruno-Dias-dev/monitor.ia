import mysql.connector
import os
from flask import request, jsonify, Blueprint


# def conectar_db_avaliacoes():
#     return mysql.connector.connect(
#         host=os.environ["DB_HOST2"],
#         port=int(os.environ["DB_PORT2"]),
#         user=os.environ["DB_USER2"],
#         password=os.environ["DB_PASSWORD2"],
#         database=os.environ["DB_NAME2"]
#     )

registro_bp = Blueprint("registro", __name__)


@registro_bp.route("/registro", methods=["POST"])
def registro():
    dados = request.get_json()
    print(dados)

    if not dados:
        return jsonify({"error": "Dados nÃ£o fornecidos"})

    return jsonify({
        "ok": True,
        "message": "Dados recebidos com sucesso"
    }), 200



# try:
#     db = conectar_db_avaliacoes
#     cursor = db.cursor()
#     cursor.execute(
#         """INSERT INTO avaliacao_atendimentos (identificador_unico, data, conversacao, canal, contemplado, beneficiario, numero, saudacao, clareza, conhecimento, resolucao, empatia, score_qualidade, risco_processo, resolvido, reincidencia, observacoes, acao_gerencial, criado_em)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
#     )

#         db.commit()

#         return jsonify({
#             "ok": True,
#             "message": "Registro realizado com sucesso"
#         }), 201

# except Exception as e:
#     print("Erro:", e)

#      return jsonify({
#         "ok": False,
#         "error": str(e)
#     }), 500
# finally:
#         if 'cursor' in locals():
#           cursor.close()

#         if 'db' in locals():
#           db.close()
