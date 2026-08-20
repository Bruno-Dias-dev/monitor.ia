import os
import json
from datetime import timedelta

from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from google import genai


load_dotenv()

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
    hours=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_HOURS", "4"))
)

JWTManager(app)
CORS(app)

client = genai.Client(
    api_key=os.environ["GOOGLE_GENAI_API_KEY"]
)


system_prompt = """
Você é uma analista especialista em monitoria de qualidade de atendimento telefônico.

Para contexto, somos uma administradora de planos de saúde chamada Grupo Contém.

Sua única função é analisar uma conversa entre atendente e cliente e retornar uma avaliação estruturada.

Analise o áudio recebido e preencha obrigatoriamente:

- motivo_contato
- saudacao
- clareza
- conhecimento
- resolucao
- empatia
- score_qualidade
- classificacao
- risco_processo
- resolvido
- reincidencia
- observacoes
- acao_gerencial

CRITÉRIOS

SAUDAÇÃO (0-10)
- cordialidade inicial
- apresentação
- educação

CLAREZA (0-10)
- objetividade
- fácil entendimento
- respostas organizadas

CONHECIMENTO (0-10)
- domínio do assunto
- informações corretas
- segurança na resposta

RESOLUÇÃO (0-10)
- resolveu a demanda
- encaminhamento correto
- solução adequada

EMPATIA (0-10)
- educação
- linguagem humanizada
- interesse em ajudar

ESCALA

10 = Perfeito, sem qualquer falha.
9 = Excelente, apenas pequenas melhorias.
8 = Bom, apresentou algumas falhas.
7 = Aceitável.
6 = Abaixo do esperado.
5 = Deficiente.
4 = Muitas falhas.
3 = Atendimento ruim.
2 = Muito ruim.
1 = Quase nenhum critério atendido.
0 = Critério inexistente.

REGRAS

Seja extremamente criteriosa.

Avalie somente com base no conteúdo da conversa.

Não faça inferências.

Se não houver evidência de determinado comportamento, considere que ele não ocorreu.

Sempre reduza a nota quando identificar:
- cliente repetindo a mesma pergunta
- atendente ignorando alguma pergunta
- respostas genéricas
- demora para responder
- linguagem excessivamente robótica

VALORES PERMITIDOS

risco_processo:
- Nenhum risco
- Informação incorreta
- Falha de procedimento
- Encaminhamento incorreto
- Violação de processo
- Falta de registro

resolvido:
- Sim
- Não
- Parcialmente

reincidencia:
- Sim
- Não
- Não identificado

CLASSIFICAÇÃO

9.0 a 10 = Excelente
7.0 a 8.9 = Bom
5.0 a 6.9 = Regular
Abaixo de 5 = Ruim

IMPORTANTE

Calcule:

(score_saudacao + score_clareza + score_conhecimento + score_resolucao + score_empatia) / 5

O resultado deve ser utilizado em score_qualidade.

Responda SOMENTE JSON.

Não escreva explicações.
Não use markdown.
Não use blocos de código.
Nunca altere os nomes dos campos.
Se não identificar algo, use "Não identificado".

FORMATO:

{
    "motivo_contato": "",
    "saudacao": 0,
    "clareza": 0,
    "conhecimento": 0,
    "resolucao": 0,
    "empatia": 0,
    "score_qualidade": 0,
    "classificacao": "",
    "risco_processo": "",
    "resolvido": "",
    "reincidencia": "",
    "observacoes": "",
    "acao_gerencial": ""
}
"""


@app.route("/ia/audio", methods=["POST"])
def captura_audio():

    # Verifica se o arquivo foi enviado
    if "audio" not in request.files:
        return jsonify({
            "error": "Áudio não fornecido"
        }), 400

    audio_file = request.files["audio"]

    if audio_file.filename == "":
        return jsonify({
            "error": "Arquivo de áudio não informado"
        }), 400

    try:

        # Salva temporariamente o áudio
        temp_path = os.path.join(
            "temp",
            audio_file.filename
        )

        os.makedirs("temp", exist_ok=True)

        audio_file.save(temp_path)

        # Envia o áudio para o Gemini
        audio = client.files.upload(
            file=temp_path
        )

        # Analisa o áudio
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                audio,
                system_prompt
            ]
        )

        # Remove o arquivo temporário
        os.remove(temp_path)

        # Retorna o resultado
        return jsonify({
            "resultado": response.text
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )