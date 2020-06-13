from flask import Blueprint, request

from api.commons.mails import send

mails = Blueprint('mails', __name__)


@mails.route('/mail', methods=['POST'])
def send_email():
    to = request.form.get('to')
    subject = request.form.get('subject')
    text = request.form.get('text')
    html = request.form.get('html')
    return send(to, subject, text, html)
