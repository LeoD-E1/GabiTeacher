import requests
import json

from commons.env import env

url = env.get('TRUSTIFI_URL')
headers = {
    'x-trustifi-key': env.get('TRUSTIFI_KEY'),
    'x-trustifi-secret': env.get('TRUSTIFI_SECRET'),
    'Content-Type': 'application/json'
}


def SendEmail():
    body = {
        "recipients": [{"email": "leandro.cotti@widergy.com", "name": "test", "phone": {"country_code": "+1", "phone_number": "1111111111"}}],
        "lists": [],
        "contacts": [],
        "attachments": [],
        "title": "Title",
        "html": "Body",
        "methods": {
            "postmark": False,
            "secureSend": False,
            "encryptContent": False,
            "secureReply": False
        }
    }
    response = requests.request(
        'POST', url, headers=headers, data=str(body))
    print(response.json())
    return response.json()
