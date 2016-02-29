import os
os.environ['DEBUG'] = "1"

# patch rfc6749 for twitch
import oauthlib.oauth2.rfc6749.parameters
orig_val_func = oauthlib.oauth2.rfc6749.parameters.validate_token_parameters

def new_val_func(params, scope=None):
    if 'token_type' not in params:
        params['token_type'] = ''
    return orig_val_func(params, scope)

oauthlib.oauth2.rfc6749.parameters.validate_token_parameters = new_val_func

import requests
import json
from flask import Flask, render_template
from flask import Blueprint, Response
from flask import request, redirect, session, escape, jsonify, g, url_for
from requests_oauthlib import OAuth2Session
from .config import secret_key, client_id, client_secret


def create_app():
    app = Flask(__name__)
    app.secret_key = secret_key

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        """
        Remove the thread local session when the web request ends.
        """
        pass

    # @app.errorhandler(404)
    # def page_not_found(e):
    #    return render_template('404.html'), 404

    foo = Blueprint("foo", "foo")

    @foo.route("/", methods=["GET"])
    def site_index():
        return "This is site index.", 200

    authorization_base_url = 'https://api.twitch.tv/kraken/oauth2/authorize'
    token_url = 'https://api.twitch.tv/kraken/oauth2/token'
    #redirect_uri = 'http://localhost/twitchapp/callback'
    redirect_uri = 'http://localhost:5000/callback'
    #auth_scope = ["user_read","channel_read","channel_editor","chat_login"]
    auth_scope = ["channel_editor"]

    @foo.route("/login")
    def login():
        twitch = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=auth_scope)
        authorization_url, state = twitch.authorization_url(authorization_base_url)

        session['oauth_state'] = state
        return redirect(authorization_url)

    @foo.route("/callback")
    def callback():
        twitch = OAuth2Session(client_id, redirect_uri=redirect_uri, state=session['oauth_state'], scope=auth_scope)
        token = twitch.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)

        return jsonify(token), 200

    app.register_blueprint(foo)
    return app
