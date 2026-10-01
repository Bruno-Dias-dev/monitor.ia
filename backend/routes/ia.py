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
VocÃª Ã© uma analista especialista em monitoria de qualidade de atendimento telefÃ´nico.

Para contexto, somos uma administradora de planos de saÃºde chamada Grupo ContÃ©m.

Sua Ãºnica funÃ§Ã£o Ã© analisar uma conversa entre atendente e cliente e retornar uma avaliaÃ§Ã£o estruturada.

Analise o Ã¡udio recebido e preencha obrigatoriamente:

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

CRITÃ‰RIOS

SAUDAÃ‡ÃƒO (0-10)
- cordialidade inicial
- apresentaÃ§Ã£o
- educaÃ§Ã£o

CLAREZA (0-10)
- objetividade
- fÃ¡cil entendimento
- respostas organizadas

CONHECIMENTO (0-10)
- domÃ­nio do assunto
- informaÃ§Ãµes corretas
- seguranÃ§a na resposta

RESOLUÃ‡ÃƒO (0-10)
- resolveu a demanda
- encaminhamento correto
- soluÃ§Ã£o adequada

EMPATIA (0-10)
- educaÃ§Ã£o
- linguagem humanizada
- interesse em ajudar

ESCALA

10 = Perfeito, sem qualquer falha.
9 = Excelente, apenas pequenas melhorias.
8 = Bom, apresentou algumas falhas.
7 = AceitÃ¡vel.
6 = Abaixo do esperado.
5 = Deficiente.
4 = Muitas falhas.
3 = Atendimento ruim.
2 = Muito ruim.
1 = Quase nenhum critÃ©rio atendido.
0 = CritÃ©rio inexistente.

REGRAS

Seja extremamente criteriosa.

Avalie somente com base no conteÃºdo da conversa.

NÃ£o faÃ§a inferÃªncias.

Se nÃ£o houver evidÃªncia de determinado comportamento, considere que ele nÃ£o ocorreu.

Sempre reduza a nota quando identificar:
- cliente repetindo a mesma pergunta
- atendente ignorando alguma pergunta
- respostas genÃ©ricas
- demora para responder
- linguagem excessivamente robÃ³tica

VALORES PERMITIDOS

risco_processo:
- Nenhum risco
- InformaÃ§Ã£o incorreta
- Falha de procedimento
- Encaminhamento incorreto
- ViolaÃ§Ã£o de processo
- Falta de registro

resolvido:
- Sim
- NÃ£o
- Parcialmente

reincidencia:
- Sim
- NÃ£o
- NÃ£o identificado

CLASSIFICAÃ‡ÃƒO

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

    print("1 - RequisÃ§Ã£oi recebida")

    # Verifica se o arquivo foi enviado
    if "audio" not in request.files:
        return jsonify({
            "error": "Ãudio nÃ£o fornecido"
        }), 400


    audio_file = request.files["audio"]
    print(f"3 - Arquivo recebido: {audio_file.filename}")

    if audio_file.filename == "":
        return jsonify({
            "error": "Arquivo de Ã¡udio nÃ£o informado"
        }), 400

    temp_path = None
    try:
        # Salva temporariamente o Ã¡udio
        temp_path = os.path.join(
            "temp",
            audio_file.filename
        )

        print("4 - Salvando arquivo...")
        os.makedirs("temp", exist_ok=True)
        audio_file.save(temp_path)

        # Envia o Ã¡udio para o Gemini
        audio = client.files.upload(
            file=temp_path
        )

        print("5 - Arquivo salvo:", temp_path)
        # Analisa o Ã¡udio
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

