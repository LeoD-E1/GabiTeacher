from flask import render_template, Blueprint, session
import json
from routes.auth import auth

page = Blueprint('page', __name__)


@page.route('/contact')
def contact():
    return render_template('contact.html')


@page.route('/')
def home():
    return render_template('index.html')


@page.route('/dashboard')
@auth
def dashboard():
    return render_template('profile-user.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))


global page
