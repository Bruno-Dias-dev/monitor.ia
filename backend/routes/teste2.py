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

    identificadorUnico = dados.get("identificador_unico")
    data = dados.get("data")
    conversacao = dados.get("conversacao")
    canal = dados.get("canal")
    contemplado = dados.get("contemplado")
    beneficiario = dados.get("beneficiario")
    numero = dados.get("numero")
    motivoContato = dados.get("motivo_contato")
    saudacao = dados.get("saudacao")
    clareza = dados.get("clareza")
    conhecimento = dados.get("conhecimento")
    resolucao = dados.get("resolucao")
    empatia = dados.get("empatia")
    scoreQualidade = dados.get("score_qualidade")
    classificacao = dados.get("classificacao")
    riscoProcesso = dados.get("risco_processo")
    resolvido = dados.get("resolvido")
    reincidencia = dados.get("reincidencia")
    observacoes = dados.get("observacoes")
    acaoGerencial = dados.get("acao_gerencial")
    criadoEm = dados.get("criado_em")

    try:
        db = conectar_db_avaliacoes
        cursor = db.cursor()
        cursor.execute(
            """INSERT INTO avaliacao_atendimentos (
                identificador_unico, data, conversacao, canal, contemplado,
                beneficiario, numero, saudacao, clareza, conhecimento,
                resolucao, empatia, score_qualidade, risco_processo,
                resolvido, reincidencia, observacoes, acao_gerencial, criado_em
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s
            )""",
            (
                identificadorUnico,
                data,
                conversacao,
                canal,
                contemplado,
                beneficiario,
                numero,
                saudacao,
                clareza,
                conhecimento,
                resolucao,
                empatia,
                scoreQualidade,
                riscoProcesso,
                resolvido,
                reincidencia,
                observacoes,
                acaoGerencial,
                criadoEm,
            ),
        )
    except Exception as e:
        print("Erro:", e)

    # db.commit()

    # return jsonify({
    #     "ok": True,
    #     "message": "Registro realizado com sucesso"
    # }), 201

    # finally:
    #     if 'cursor' in locals():
    #         cursor.close()
    #     if 'db' in locals():
    #         db.close()
