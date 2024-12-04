import requests


def request_api(url, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    if response.status_code == 200:
        return response.json()
