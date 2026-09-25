import os
import requests
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

# Rodando variáveis de ambiente
load_dotenv()
url = os.getenv("EXCEL_URL")

# Captura do Excel
def capturaExcel():
    response = requests.get(url)
    response.raise_for_status()
    df = pd.read_excel(BytesIO(response.content), sheet_name="media")

#   pd.set_option("display.max_columns", None)

    df_avaliacoes = pd.read_excel(BytesIO(response.content), sheet_name="media")

    dados = {}
    # Para cada linha da planilha,, pegue os dados 
    for _, pessoa in df_avaliacoes.iterrows():

        nome = pessoa["Contemplado"]

        dados[nome] = {
            "nome": nome,
            "media_saudacao": pessoa["Média Saudação"],
            "media_clareza": pessoa["Média Clareza"],
            "media_conhecimento": pessoa["Média Conhecimento"],
            "media_empatia": pessoa["Média Empatia"],
            "media_resolucao": pessoa["Média Resolução"]
        }

    return dados

app = Flask(__name__)
CORS(app)

@app.route("/avaliacoes/media", methods=["GET"])
def avaliacoes_media():
    dados = capturaExcel()

    return jsonify(dados)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5003,
        debug=True)

