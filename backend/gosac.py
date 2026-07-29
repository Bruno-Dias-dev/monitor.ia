import os

import requests
from dotenv import load_dotenv

load_dotenv()

def buscar_gosac():

    url = os.environ["GOSAC_API_URL"]

    params = {
        "startPeriod": os.environ["GOSAC_START_PERIOD"],
        "endPeriod": os.environ["GOSAC_END_PERIOD"]
    }

    headers = {
        "Authorization": os.environ["GOSAC_API_TOKEN"]
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