from api.commons.mails import send


def send_email(req):
    to = req['body']['to']
    subject = req['body']['subject']
    text = req['body']['text']
    html = req['body']['html']
    result = send(to, subject, text, html)
    return {'status': 200, 'body': result}
