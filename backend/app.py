import os
from datetime import datetime, time, timedelta

import mysql.connector
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import check_password_hash

from gosac import buscar_gosac
from chatwoot import buscar_chatwoot

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_HOURS", "4")))
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"

jwt = JWTManager(app)


def conectar_db():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.getenv("DB_NAME", "grupocontem"),
        auth_plugin="mysql_native_password"
    )


def verificar_senha(db_password, senha_recebida):
    if db_password == senha_recebida:
        return True
    try:
        return check_password_hash(db_password, senha_recebida)
    except ValueError:
        return False


@app.route("/webhook/login", methods=["POST"])
def login():
    dados = request.get_json(silent=True)
    if not dados:
        return jsonify({"ok": False, "error": "JSON inválido ou não fornecido"}), 400

    email = dados.get("email")
    senha = dados.get("senha")

    if not email or not senha:
        return jsonify({"ok": False, "error": "Email e senha são obrigatórios"}), 400

    try:
        db = conectar_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, nome, email, senha FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user or not verificar_senha(user["senha"], senha):
            return jsonify({"ok": False, "error": "Login inválido"}), 401

        token = create_access_token(identity=user["id"], additional_claims={"email": user["email"]})

        return jsonify({
            "ok": True,
            "token": token,
            "usuario": {
                "id": user["id"],
                "nome": user["nome"],
                "email": user["email"]
            }
        })
    except mysql.connector.Error as error:
        return jsonify({"ok": False, "error": "Erro de banco de dados", "detail": str(error)}), 500
    except Exception as error:
        return jsonify({"ok": False, "error": "Erro interno", "detail": str(error)}), 500
    finally:
        if "cursor" in locals():
            cursor.close()
        if "db" in locals():
            db.close()


@app.route("/api/dashboard")
@jwt_required()
def dashboard():
    gosac = buscar_gosac()
    chatwoot = buscar_chatwoot()
    return jsonify({"chatwoot": chatwoot})


@app.route("/api/me")
@jwt_required()
def me():
    return jsonify({"ok": True, "id": get_jwt_identity()})


@app.route("/api/avaliacoes", methods=["GET"])
@jwt_required()
def consultar_avaliacoes():
    data_inicial = request.args.get("data_inicial", "").strip()
    data_final = request.args.get("data_final", "").strip()

    if not data_inicial or not data_final:
        return jsonify({"ok": False, "error": "Data inicial e data final são obrigatórias"}), 400

    try:
        inicio = datetime.strptime(data_inicial, "%Y-%m-%d").date()
        fim = datetime.strptime(data_final, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"ok": False, "error": "As datas devem estar no formato AAAA-MM-DD"}), 400

    if inicio > fim:
        return jsonify({"ok": False, "error": "A data inicial não pode ser maior que a data final"}), 400

    campos = """
        id, identificador_unico, data, conversacao, canal, contemplado,
        beneficiario, numero, saudacao, clareza, conhecimento, resolucao,
        empatia, score_qualidade, risco_processo, resolvido, reincidencia,
        observacoes, acao_gerencial, criado_em
    """

    try:
        db = conectar_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            f"""
            SELECT {campos}
            FROM avaliacao_atendimentos
            WHERE data >= %s AND data <= %s
            ORDER BY data DESC, id DESC
            """,
            (datetime.combine(inicio, time.min), datetime.combine(fim, time.max))
        )
        return jsonify({"ok": True, "registros": cursor.fetchall()})
    except mysql.connector.Error:
        return jsonify({"ok": False, "error": "Erro ao consultar as avaliações"}), 500
    finally:
        if "cursor" in locals():
            cursor.close()
        if "db" in locals():
            db.close()


@jwt.unauthorized_loader
def unauthorized_callback(_):
    return jsonify({"ok": False, "error": "Token ausente ou inválido"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"ok": False, "error": "Token inválido", "detail": error}), 401


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"ok": False, "error": "Token expirado"}), 401


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
