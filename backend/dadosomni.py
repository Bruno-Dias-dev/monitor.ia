from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required
from flask_cors import CORS
from chatwoot import buscar_chatwoot

app = Flask(__name__)

CORS(app)

@app.route("/api/dashboard", methods=["GET"])
# ,@jwt_required()

def dashboard():
    chatwoot = buscar_chatwoot()


    return jsonify({
        "chatwoot": chatwoot
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
