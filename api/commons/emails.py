import requests
import json
from requests.auth import HTTPBasicAuth

from api.commons.env import env

api_key = env.get('MAILGUN_API_KEY')
domain = env.get('MAILGUN_DOMAIN')
url = f'https://api.mailgun.net/v3/{domain}/messages'


def send(from_email, to, subject, text, html):
    body = {
        'from': from_email,
        'to': to,
        'subject': subject,
        'text': text,
        'html': html
    }
    response = requests.request(
        'POST', url, data=body, auth=HTTPBasicAuth('api', api_key))
    return {'status': response.status_code, 'body': response.json()}
