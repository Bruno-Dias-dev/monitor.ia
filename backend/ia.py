from google import genai

client = genai.Client(api_key="AQ.Ab8RN6KHY2YjTH7kyoIqeNJQ7E5QxoileR3gfFuSzNYLFh7nAg")


system_prompt = """
Você é um desenvolvedor Python sênior.
Sempre responda em português.
Meu nome é gostosa
"""

texto_usuario = """
O que é CRUD? Explique usando Flask.
"""
prompt = f"""
{system_prompt}

Pergunta do usuário:
{texto_usuario}
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)


print(response.text)