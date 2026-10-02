import os
import json
from datetime import timedelta
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from google import genai

ia_bp = Blueprint("ia", __name__)

client = genai.Client(
    api_key=os.environ["GOOGLE_GENAI_API_KEY"]
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

(score_saudacao + score_clareza + score_conhecimento + score_resolucao + score_empatia) / 5

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
    usuario_id = get_jwt_identity()

    print("1 - Requisição recebida")

    # Verifica se o arquivo foi enviado
    if "audio" not in request.files:
        return jsonify({
            "error": "Audio nÃo fornecido"
        }), 400


    audio_file = request.files["audio"]
    print(f"3 - Arquivo recebido: {audio_file.filename}")

    if audio_file.filename == "":
        return jsonify({
            "error": "Arquivo de Áudio nÃo informado"
        }), 400

    temp_path = None
    try:
        # Salva temporariamente o Áudio
        temp_path = os.path.join(
            "temp",
            audio_file.filename
        )

        print("4 - Salvando arquivo...")
        os.makedirs("temp", exist_ok=True)
        audio_file.save(temp_path)

        # Envia o Áudio para o Gemini
        audio = client.files.upload(
            file=temp_path
        )

        print("5 - Arquivo salvo:", temp_path)
        # Analisa o Audio
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                audio,
                system_prompt
            ]
        )

        print("7 - Arquivo enviado para Gemini")
        print("10 - Retornando resposta para navegador")

        # Retorna o resultado
        return jsonify({
            "resultado": response.text,
            "usuario_id": usuario_id
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
        # Remove o arquivo temporario, mesmo quando ocorrer erro.
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

