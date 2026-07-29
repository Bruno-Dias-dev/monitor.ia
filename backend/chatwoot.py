import os

import requests
from dotenv import load_dotenv

load_dotenv()

def buscar_chatwoot():

    url = os.environ["CHATWOOT_API_URL"]

    headers = {
        "api_access_token": os.environ["CHATWOOT_API_TOKEN"]
    }

    params = {
        "type": "account"
    }

    response = requests.get (
        url,
        headers = headers,
        params = params
    )

    response.raise_for_status()

    return {
        "chatwoot": response.json()
    }