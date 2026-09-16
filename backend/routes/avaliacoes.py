import json
from datetime import date, datetime
from decimal import Decimal

import mysql.connector
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required

from database import abrir_conexao

avaliacoes_bp = Blueprint("avaliacoes", __name__, url_prefix="/api")

CONSULTA_AVALIACOES = """
    SELECT id, identificador_unico, data, canal, contemplado, beneficiario,
           numero, saudacao, clareza, conhecimento, resolucao, empatia,
           score_qualidade, risco_processo, resolvido, reincidencia,
           observacoes, acao_gerencial, conversacao, criado_em
    FROM avaliacao_atendimentos
    WHERE data >= %s
      AND data < DATE_ADD(%s, INTERVAL 1 DAY)
    ORDER BY data DESC
"""


def validar_periodo(data_inicial, data_final):
    if not data_inicial:
        return None, "O parâmetro data_inicial é obrigatório."
    if not data_final:
        return None, "O parâmetro data_final é obrigatório."
    try:
        inicio = datetime.strptime(data_inicial, "%Y-%m-%d").date()
        fim = datetime.strptime(data_final, "%Y-%m-%d").date()
    except ValueError:
        return None, "As datas devem estar no formato YYYY-MM-DD."
    if inicio > fim:
        return None, "A data inicial não pode ser maior que a data final."
    return (inicio, fim), None


def serializar_valor(valor):
    if isinstance(valor, (datetime, date)):
        return valor.isoformat()
    if isinstance(valor, Decimal):
        return float(valor)
    if isinstance(valor, bytes):
        return valor.decode("utf-8", errors="replace")
    return valor


def preparar_registro(registro):
    registro = {campo: serializar_valor(valor) for campo, valor in registro.items()}
    conversa = registro.get("conversacao")
    if isinstance(conversa, str):
        try:
            registro["conversacao"] = json.loads(conversa)
        except json.JSONDecodeError:
            pass  # TEXT que não é JSON válido: preserva o conteúdo original.
    return registro


@avaliacoes_bp.get("/avaliacoes")
# Teste temporário sem JWT. Antes de publicar, remova o comentário abaixo.
# @jwt_required()
def consultar_avaliacoes():
    data_inicial = request.args.get("data_inicial", "").strip()
    data_final = request.args.get("data_final", "").strip()
    periodo, erro = validar_periodo(data_inicial, data_final)
    if erro:
        return jsonify({"error": erro}), 400

    conexao = cursor = None
    try:
        conexao = abrir_conexao()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(CONSULTA_AVALIACOES, periodo)
        registros = [preparar_registro(registro) for registro in cursor.fetchall()]
        return jsonify({"registros": registros}), 200
    except mysql.connector.Error:
        current_app.logger.exception("Erro do MySQL ao consultar avaliações")
        return jsonify({"error": "Não foi possível consultar as avaliações."}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if conexao is not None and conexao.is_connected():
            conexao.close()
