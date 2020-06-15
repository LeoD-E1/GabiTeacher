from flask import render_template, session
import json
from api.routes.auth import auth


def contact(req):
    return render_template('contact.html')


def home(req):
    return render_template('index.html')


@auth
def dashboard(req):
    return render_template('profile-user.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))
