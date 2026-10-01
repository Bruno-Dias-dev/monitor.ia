import os
import mysql.connector
from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token

login_bp = Blueprint("login", __name__)

def conectar_db():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"]
    )


@login_bp.route("/webhook/login", methods=["POST"])
def login():
    dados = request.get_json()
    
    if not dados:
        return jsonify({"error": "Dados não fornecidos"}), 400
    
    email = dados.get("email")
    senha = dados.get("senha")

    try:
        db = conectar_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM usuarios WHERE email = %s AND senha = %s", (email, senha)
        )
    
        user = cursor.fetchone()

        if user:
            token = create_access_token(identity=str(user[0]))
            return jsonify({
                "ok": True,
                "token": token,
                "usuario": {
                    "id": user[0],
                    "nome": user[1],
                    "email": user[2]
                }
            })
        else:
            return jsonify({
                "ok": False,
                "error": "Login inválido"
            }), 401

    except Exception as e:
        print("ERRO:", e)
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500

    finally:
        if 'db' in locals():
            db.close()


