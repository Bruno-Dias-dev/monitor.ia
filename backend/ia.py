import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ["GOOGLE_GENAI_API_KEY"])


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