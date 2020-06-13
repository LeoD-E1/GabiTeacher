"""Python Flask WebApp Auth0 integration example
"""
from flask import Flask, jsonify, redirect
from flask import session, url_for

import json
from werkzeug.exceptions import HTTPException
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

from api.commons.env import env
from api.routes.page import page
from api.routes.mails import mails

callback_url = env.get('AUTH0_CALLBACK_URL')
client_id = env.get('AUTH0_CLIENT_ID')
client_secret = env.get('AUTH0_CLIENT_SECRET')
domain = env.get('AUTH0_DOMAIN')
base_url = 'https://' + domain
audience = env.get('AUTH0_AUDIENCE')

app = Flask(__name__, static_url_path='/public', static_folder='./public')
app.register_blueprint(page)
app.register_blueprint(mails)
app.secret_key = env.get('SECRET_KEY')
app.debug = True


@app.errorhandler(Exception)
def handle_auth_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    return response


oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=client_id,
    client_secret=client_secret,
    api_base_url=base_url,
    access_token_url=base_url + '/oauth/token',
    authorize_url=base_url + '/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)


@app.route('/callback')
def callback_handling():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/dashboard')


@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=callback_url, audience=audience)


@app.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': url_for(
        'page.home', _external=True), 'client_id': client_id}
    print('logout', params)
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=env.get('PORT', 3000))
