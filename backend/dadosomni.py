from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import CORS
from chatwoot import buscar_chatwoot

app = Flask(__name__)
CORS(app)

@app.route("/api/dashboard", methods=["GET"])
@jwt_required()

def dashboard():

    usuario_id = get_jwt_identity()

    chatwoot = buscar_chatwoot()


    return jsonify({
        "usuario_id": usuario_id,
        "chatwoot": chatwoot
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
