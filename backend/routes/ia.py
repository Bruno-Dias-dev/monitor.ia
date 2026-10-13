import os
import json
import uuid
from datetime import datetime
import mysql.connector
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required
from google import genai
from werkzeug.utils import secure_filename
from random import randint

numero_0a10000 = randint(0, 10000)

ia_bp = Blueprint("ia", __name__)

# Rodando variáveis de ambiente
apiKey = os.getenv("GOOGLE_GENAI_API_KEY")


client = genai.Client(
    api_key=apiKey
)


def conectar_db_avaliacoes():
    return mysql.connector.connect(
        host=os.environ["DB_HOST2"],
        port=int(os.environ["DB_PORT2"]),
        user=os.environ["DB_USER22"],
        password=os.environ["DB_PASSWORD2"],
        database=os.environ["DB_NAME2"]
    )

system_prompt = """
Você é uma analista especialista em monitoria de qualidade de atendimento telefônico.

Para contexto, somos uma administradora de planos de saúde chamada Grupo Contém.

Sua única função a analisar uma conversa entre atendente e cliente e retornar uma avaliação estruturada.

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
- domí­nio do assunto
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
1 = Quase nenhum critÃ©rio atendido.
0 = Critério inexistente.

REGRAS

Seja extremamente criteriosa.

Avalie somente com base no conteúdo da conversa.

NÃo faça inferências.

Se nÃo houver evidência de determinado comportamento, considere que ele nÃo ocorreu.

Sempre reduza a nota quando identificar:
- cliente repetindo a mesma pergunta
- atendente ignorando alguma pergunta
- respostas genêricas
- demora para responder
- linguagem excessivamente robotica

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
- NÃ£o
- Parcialmente

reincidencia:
- Sim
- NÃ£o
- NÃ£o identificado

CLASSIFICAÇÃO

9.0 a 10 = Excelente
7.0 a 8.9 = Bom
5.0 a 6.9 = Regular
Abaixo de 5 = Ruim

IMPORTANTE

Calcule:

(saudacao + clareza + conhecimento + resolucao + empatia) / 5

O resultado deve ser utilizado em score_qualidade.

Responda SOMENTE JSON.

NÃ£o escreva explicaÃ§Ãµes.
NÃ£o use markdown.
NÃ£o use blocos de cÃ³digo.
Nunca altere os nomes dos campos.
Se nÃ£o identificar algo, use "NÃ£o identificado".

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


@ia_bp.route("/ia/audio", methods=["POST"])
@jwt_required()


def captura_audio():
    # usuario_id = get_jwt_identity()

    print("1 - Requisição recebida")

    cliente = request.form.get("cliente", "").strip()
    contemplado = request.form.get("contemplado", "").strip()
    data = request.form.get("data", "").strip()
    numero = request.form.get("numero", "").strip()

    print(data, cliente, contemplado, numero)

    # Verifica se o arquivo foi enviado
    if "audio" not in request.files:
        return jsonify({
            "error": "Audio nÃo fornecido"
        }), 400
    
    if not cliente or not contemplado or not data:
        return jsonify({
            "error": "Texto não fornecido"
        }), 400


    audio_file = request.files["audio"]
    print(f"3 - Arquivo recebido: {audio_file.filename}")

    if audio_file.filename == "":
        return jsonify({
            "error": "Arquivo de Áudio nÃo informado"
        }), 400

    temp_path = None
    db = None
    cursor = None

    try:
        # Salva temporariamente o Áudio
        temp_path = os.path.join(
            "temp",
            secure_filename(audio_file.filename)
        )

        print("4 - Salvando arquivo...")
        os.makedirs("temp", exist_ok=True)
        audio_file.save(temp_path)

        # Envia o Áudio para o Gemini
        audio = client.files.upload(file=temp_path)

        print("5 - Arquivo salvo:", temp_path)
        # Analisa o Audio
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=[audio, system_prompt],
            config={"response_mime_type": "application/json"},
        )
        resultado = json.loads(response.text)

        print("7 - Arquivo enviado para Gemini")
        print("10 - Retornando resposta para navegador")

        canal = "55PABX"
        conversacao = json.dumps("audio")


        db = conectar_db_avaliacoes()
        cursor = db.cursor()
        cursor.execute(
            """INSERT INTO avaliacao_atendimentos (
                identificador_unico, data, conversacao, canal, contemplado,
                beneficiario, numero, saudacao, clareza, conhecimento,
                resolucao, empatia, score_qualidade, risco_processo, resolvido,
                reincidencia, observacoes, acao_gerencial, criado_em
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                numero_0a10000,
                data,
                conversacao,
                canal,
                contemplado,
                cliente,
                numero,
                resultado["saudacao"],
                resultado["clareza"],
                resultado["conhecimento"],
                resultado["resolucao"],
                resultado["empatia"],
                resultado["score_qualidade"],
                resultado["risco_processo"],
                resultado["resolvido"],
                resultado["reincidencia"],
                resultado["observacoes"],
                resultado["acao_gerencial"],
                datetime.now(),
            ),
        )
        db.commit()

        # Retorna o resultado
        return jsonify({
            "resultado": resultado
#            "usuario_id": usuario_id
        }), 200

    except Exception as e:
        print("ERRO:", repr(e))

        erro = str(e)

        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            return jsonify({
                "erro": "Limite do uso da IA excedido.",
                "detalhamento": erro
            }), 429

        return jsonify({
            "error": "Erro ao processar o Ã¡udio.",
            "detalhamento": erro
        }), 500

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None and db.is_connected():
            db.close()
        # Remove o arquivo temporario, mesmo quando ocorrer erro.
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

