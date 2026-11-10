import os
import json
import logging
import tempfile
import uuid
from datetime import datetime
import mysql.connector
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required
from google import genai
from werkzeug.utils import secure_filename
from random import randint
from simpleeval import simple_eval


numero_0a10000 = randint(0, 10000)

ia_bp = Blueprint("ia", __name__)
logger = logging.getLogger(__name__)

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

# TOOL CALCULATOR
def calculator(expressao: str) -> float:
    return round(simple_eval(expressao), 2)

system_prompt = """
# Identidade

Você é uma analista especialista em monitoria de qualidade de atendimento omnichannel.

# Personalidade e Contexto
- Você é uma analista especialista em monitoria de qualidade de atendimento omnichannel.
- Para contexto, somos uma administradora de planos de saúde chamada Grupo Contém. 
- Sua única função é analisar uma conversa entre atendente e cliente e retornar uma avaliação estruturada.

# Tarefa
Analise a conversa recebida.

Preencha obrigatoriamente os seguintes campos:

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

# Critérios de avaliação

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

# Escala obrigatória
Defina exatemente a estrutura das notas dessa forma: 
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

# Regra de Avaliação


## Regra geral de rigor
Seja extremamente criteriosa. A nota máxima (10) representa um atendimento excepcional e praticamente sem qualquer falha.

Em caso de dúvida, atribua a menor nota compatível com as evidências.

Nunca presuma que algo aconteceu se não estiver explicitamente registrado na conversa.

## Regra de Evidência 
Avalie somente com base no conteúdo da conversa.

Não faça inferências.

Se não houver evidência de determinado comportamento, considere que ele não ocorreu.

## Regra de penalização obrigatória
Sempre reduza a nota quando identificar:
- Cliente precisa repetir a mesma pergunta -1 ponto
- Atendente ignora alguma pergunta -1 ponto
- Respostas genéricas -1 ponto
- Linguagem excessivamente robótica -1 ponto
- Demonstra desconhecimento do procedimento -1 ponto
- Transfere o problema sem orientação -1 ponto
- Fornece informação incompleta -1 ponto

### Observações
1. Cada ocorrência identificada desconta 1 ponto da nota do critério relacionado.
2. Quando uma mesma falha ocorrer várias vezes, cada ocorrência deve gerar um novo desconto.
3. Falhas diferentes devem ter seus descontos acumulados.
4. A nota mínima permitida é 0.
5. Não aplique o mesmo desconto duas vezes pelo mesmo comportamento.
6. Não deixe de penalizar uma falha por o restante do atendimento ter sido satisfatório.
7. Não aplique penalizações sem evidências explícitas na conversa.
8. Os descontos devem ser realizados antes do cálculo da média final.

# Cálculo de score
Sempre utilize a tool Calculator para realizar cálculos.

Nunca realize cálculos manualmente.

Calcule obrigatoriamente:

(score_saudacao + score_clareza + score_conhecimento + score_resolucao + score_empatia) / 5

O valor retornado pela Calculator deve ser utilizado em score_qualidade.


# Valores permitidos

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

# Regras importantes
* Utilize obrigatoriamente a ferramenta Calculator para realizar qualquer cálculo.
* Responder SOMENTE JSON
* Não escrever explicações
* Não adicionar texto antes ou depois
* Não usar markdown
* Não usar blocos de código
* Nunca alterar nomes dos campos
* Se não identificar algo, usar "Não identificado"

FORMATO DE SAÍDA OBRIGATÓRIO

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

    request_id = uuid.uuid4().hex[:8]
    etapa = 'validar_requisicao'
    logger.info('audio_request=%s etapa=%s', request_id, etapa)

    cliente = request.form.get("cliente", "").strip()
    contemplado = request.form.get("contemplado", "").strip()
    data = request.form.get("data", "").strip()
    numero = request.form.get("numero", "").strip()

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
    if audio_file.filename == "":
        return jsonify({
            "error": "Arquivo de Áudio nÃo informado"
        }), 400

    temp_path = None
    db = None
    cursor = None

    try:
        # Salva temporariamente o Áudio
        etapa = 'salvar_audio_temporario'
        logger.info('audio_request=%s etapa=%s', request_id, etapa)
        extensao = os.path.splitext(secure_filename(audio_file.filename))[1]
        with tempfile.NamedTemporaryFile(
            prefix="monitor-ia-",
            suffix=extensao,
            delete=False,
        ) as arquivo_temporario:
            temp_path = arquivo_temporario.name
        audio_file.save(temp_path)

        # Envia o Áudio para o Gemini
        etapa = 'enviar_audio_gemini'
        logger.info('audio_request=%s etapa=%s', request_id, etapa)
        audio = client.files.upload(file=temp_path)

        # Analisa o Audio
        etapa = 'gerar_avaliacao_gemini'
        logger.info('audio_request=%s etapa=%s', request_id, etapa)
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=[audio, system_prompt],
            config={
                "response_mime_type": "application/json",
                "tools": [calculator]
            })
        etapa = 'interpretar_resposta_gemini'
        resultado = json.loads(response.text)


        canal = "55PABX"
        conversacao = json.dumps("audio")


        etapa = 'conectar_mysql'
        logger.info('audio_request=%s etapa=%s', request_id, etapa)
        db = conectar_db_avaliacoes()
        cursor = db.cursor()
        etapa = 'gravar_avaliacao_mysql'
        logger.info('audio_request=%s etapa=%s', request_id, etapa)
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
        logger.info('audio_request=%s etapa=concluido', request_id)

        # Retorna o resultado
        return jsonify({
            "resultado": resultado
#            "usuario_id": usuario_id
        }), 200
    
        print(resultado)
    except Exception as e:
        logger.exception('audio_request=%s etapa=%s falha', request_id, etapa)

        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            return jsonify({"erro": "Limite de uso da IA excedido. Tente mais tarde.", "codigo": request_id}), 429

        return jsonify({"erro": "Falha ao processar o áudio. Informe este código ao suporte.", "codigo": request_id}), 500

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None and db.is_connected():
            db.close()
        # Remove o arquivo temporario, mesmo quando ocorrer erro.
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

