import requests
import json
from requests.auth import HTTPBasicAuth

from api.commons.env import env

api_key = env.get('MAILGUN_API_KEY')
domain = env.get('MAILGUN_DOMAIN')
user = env.get('MAIL_USER')
url = 'https://api.mailgun.net/v3/' + domain + '/messages'


def send(to, subject, text, html):
    body = {
        'from': user + ' <' + user + '@' + domain + '>',
        'to': to,
        'subject': subject,
        'text': text,
        'html': html
    }
    response = requests.request(
        'POST', url, data=body, auth=HTTPBasicAuth('api', api_key))
    return response.json()
