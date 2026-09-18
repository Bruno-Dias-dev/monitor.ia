import os
import requests
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv
from flask import Flask, jsonify

# Rodando variáveis de ambiente
load_dotenv()
url = os.getenv("EXCEL_URL")

# Captura do Excel
def capturaExcel():
    response = requests.get(url)
    response.raise_for_status()
    df = pd.read_excel(BytesIO(response.content))

#   pd.set_option("display.max_columns", None)

    df_avaliacoes = pd.read_excel(BytesIO(response.content), sheet_name="media")

    # Barbara Aparecyda
    barbara = df_avaliacoes[df_avaliacoes["Contemplado"] == "Barbara Aparecyda"]
    nomeBarbara = barbara["Contemplado"].iloc[0]
    mediaSaudacao = barbara["Média Saudação"].iloc[0]
    mediaConhecimento = barbara["Média Clareza"].iloc[0]
    mediaResolucao = barbara["Média Conhecimento"].iloc[0]
    mediaEmpatia = barbara["Média Empatia"].iloc[0]

    return {
        "nome1": nomeBarbara,
        "Média saudacao Barbara": mediaSaudacao,
        "Média Conhecimento Barbara": mediaConhecimento,
        "Média Resolução Barbara": mediaResolucao,
        "Media Empatia Barbara": mediaEmpatia
    }


app = Flask(__name__)

@app.route("avaliacoes/media", methods=["GET"])
def avaliacoes_media():
    dados = capturaExcel()

    return jsonify(dados)

if __name__ == "__main__":
    app.run(debug=True)

