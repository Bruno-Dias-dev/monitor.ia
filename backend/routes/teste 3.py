import requests

url = "http://127.0.0.1:5001/registro"

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc5MTQ4NjQ1NCwianRpIjoiY2Y2NjFiYzEtODZhZS00ZjdiLTlhMDUtNTY5MGJiMmVjZTQ0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3OTE0ODY0NTQsImNzcmYiOiI3YmNjOWZjOS0xNjgxLTRiNTQtODYwOS1mZWFlZDUwY2Q1NjMiLCJleHAiOjE3OTE1MDA4NTR9.8ZGh8osvLupgmEArF53ynZYAnzUiuC_NLN53KKydNLs"
}

dados =  {
    "identificador_unico": "TESTE-001",
    "data": "2026-10-08 14:30:00",
    "conversacao": "Cliente entrou em contato para esclarecer uma cobrança. A atendente identificou o cliente, consultou o sistema e informou que havia um boleto em aberto. O cliente solicitou o envio do boleto atualizado e a atendente realizou o envio.",
    "canal": "Chatwoot",
    "contemplado": "Sim",
    "beneficiario": "MIGUEL PINTO GABRIEL",
    "numero": "+5522996151639",

    "motivo_contato": "Cliente entrou em contato para solicitar o boleto atualizado referente à mensalidade em aberto.",

    "saudacao": 9,
    "clareza": 9,
    "conhecimento": 8,
    "resolucao": 10,
    "empatia": 9,

    "score_qualidade": 9.0,
    "classificacao": "Excelente",
    "risco_processo": "Nenhum",
    "resolvido": "Sim",
    "reincidencia": "Não identificado",

    "observacoes": "A atendente realizou a identificação do cliente, consultou o sistema, esclareceu a situação e enviou o boleto solicitado. O atendimento foi conduzido de forma clara, cordial e objetiva, com a demanda solucionada.",

    "acao_gerencial": "Nenhuma ação necessária. Manter o padrão de atendimento apresentado.",

    "criado_em": "2026-10-08 14:30:00"
}


response = requests.post(url, headers=headers, json=dados)

print("Status:", response.status_code)
print("Resposta:", response.text)




