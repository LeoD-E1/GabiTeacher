from flask import render_template, session, send_file
import json
from api.routes.auth import auth
from api.commons.env import env


def contact(req):
    return render_template('contact.html', contact_emails=env.get('CONTACT_EMAILS'))

def favicon(req):
    return send_file('public/img/favicon.png')


def home(req):
    return render_template('index.html')

def get_started(req):
    return render_template('get_started.html')

@auth
def dashboard(req):
    return render_template('profile-user.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))
