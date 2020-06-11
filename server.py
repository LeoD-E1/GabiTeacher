"""Python Flask WebApp Auth0 integration example
"""
import json
from werkzeug.exceptions import HTTPException

from flask import Flask
from flask import jsonify
from flask import redirect
from flask import session
from flask import url_for
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

from commons.env import env
from routes.page import page
from routes.auth import auth

AUTH0_CALLBACK_URL = env.get('AUTH0_CALLBACK_URL')
AUTH0_CLIENT_ID = env.get('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = env.get('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = env.get('AUTH0_DOMAIN')
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
AUTH0_AUDIENCE = env.get('AUTH0_AUDIENCE')

app = Flask(__name__, static_url_path='/public', static_folder='./public')
app.register_blueprint(page)
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
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url=AUTH0_BASE_URL + '/oauth/token',
    authorize_url=AUTH0_BASE_URL + '/authorize',
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
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)


@app.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': url_for(
        'page.home', _external=True), 'client_id': AUTH0_CLIENT_ID}
    print('logout', params)
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=env.get('PORT', 3000))
