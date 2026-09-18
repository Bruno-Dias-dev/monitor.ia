import os
import requests
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("EXCEL_URL")

response = requests.get(url)
response.raise_for_status()
# df = pd.read_excel(BytesIO(response.content))
# pd.set_option("display.max_columns", None)

df_avaliacoes = pd.read_excel(BytesIO(response.content), sheet_name="media")

print(df_avaliacoes)
