import requests

def buscar_chatwoot():

    url = "https://chatwoot.grupocontem.com.br/api/v2/accounts/1/reports/conversations"

    headers = {
        "api_access_token": "BuLinx9FJnnwMJ4s5qBzcG7V"
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