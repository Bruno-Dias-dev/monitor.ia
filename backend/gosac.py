import requests 

def buscar_gosac():

    url = "https://grupocontem.gosac.com.br/api/dashboard/general"

    params = {
        "startPeriod": "2026-06-11",
        "endPeriod": "2026-06-12"
    }

    headers = {
        "Authorization": "INTEGRATION 2f632a5dfc3153add88cd01d7ceefc00545db1e9abc8238840182beb4a23"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    print(response.json())

    response.raise_for_status()

    return {
        "gosac": response.json()
    }