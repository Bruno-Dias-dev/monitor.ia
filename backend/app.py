from flask import Flask, jsonify
from flask_cors import CORS

from gosac import buscar_gosac
from chatwoot import buscar_chatwoot

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

@app.route("/api/dashboard")
def dashboard():
    gosac = buscar_gosac()
    chatwoot = buscar_chatwoot()

    return jsonify({
        "chatwoot": chatwoot
    })

if __name__ == "__main__":
    app.run(debug=True)