import json
from flask import Blueprint

from routes.auth import auth
from commons.mails import SendEmail

mails = Blueprint('mails', __name__)


@mails.route('/mail', methods=['POST'])
def sendEmail():
    return SendEmail()


global mails
