from flask import render_template, session
import json
from api.routes.auth import auth
from api.commons.env import env


def contact(req):
    return render_template('contact.html', contact_emails=env.get('CONTACT_EMAILS'))


def home(req):
    return render_template('index.html')


@auth
def dashboard(req):
    return render_template('profile-user.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))
