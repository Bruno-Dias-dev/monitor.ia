from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
from flask_jwt_extended import create_acess_token

app = Flask(__name__)
CORS(app)

def conectar_db():
    return mysql.connector.connect(
        host="easypanel.lum3.com.br",
        port=3006,
        user= "root",
        password="Hb181020",
        database="monitor_ia"
    )

@app.route("/webhook/login", methods=["POST"])
def login():
    dados = request.get_json()
    
    print(dados)

    if not dados:
        return jsonify({"error": "Dados não fornecidos"}), 400
    
    email = dados.get("email")
    senha = dados.get("senha")

    print(email, senha)

    try:
        db = conectar_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM usuarios WHERE email = %s AND  senha = %s", (email, senha)
        )
    
        user = cursor.fetchone()


        if user:
            token = create_acess_token(identity=user[0])


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
            })

    except Exception as e:
        print("ERRO:", e)
        return jsonify({
            "ok": False,
            "error": str(e)
        })

    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    app.run(debug=True)

