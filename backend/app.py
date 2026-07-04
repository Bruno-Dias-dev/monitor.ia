from flask import Flask, jsonify

from gosac import buscar_gosac
from chatwoot import buscar_chatwoot

app = Flask(__name__)

@app.route("/api/dashboard")
def dashboard():

    gosac = buscar_gosac
    chatwoot = buscar_chatwoot

    return jsonify({
        "gosac": gosac,
        "chatwoot": chatwoot
    })