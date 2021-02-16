import os

from flask import Flask, redirect, request
from flask_oidc import OpenIDConnect
from jinja2 import Template
import logging

from config import template_directory
from helpers import functions

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)
app.config['OIDC_CLIENT_SECRETS'] = 'client_secrets.json'
app.config['OIDC_CALLBACK_ROUTE'] = '/oidc/callback'
app.config['OIDC_SCOPES'] = ['openid', 'email', 'profile', 'phone', 'aws.cognito.signin.user.admin']
app.config['SECRET_KEY'] = os.getenv('random_long_string')
app.config['OIDC_ID_TOKEN_COOKIE_NAME'] = 'token'
app.config['OIDC_TOKEN_SECURE'] = True
oidc = OpenIDConnect(app)


@app.route('/')
def root():
    if oidc.user_loggedin:
        user = oidc.user_getfield('email')
    else:
        user = None

    template_file = next(
        file for file in template_directory.iterdir() if 'index.html' == file.name.lower()
    )

    return Template(template_file.read_text()).render(
        cloudfront_url=os.getenv('cloudfront_url'),
        user=user,
        login_url='login',
        logout_url='logout',
        email_me_url='email-me',
        custom_message=None
    )


@app.route('/login')
@oidc.require_login
def login():
    return redirect('/', 302)


@app.route('/protected')
@oidc.require_login
def protected():
    return f'Hello {oidc.user_getfield("email")}'


@app.route('/logout')
def logout():
    if oidc.user_loggedin:
        oidc.logout()

    return redirect(
        functions.build_logout(),
        302
    )


@app.route('/email-me', methods=['POST'])
def email_me():
    functions.email(
        name=request.form['name'],
        email_address=request.form['email'],
        subject=request.form['subject'],
        message=request.form['message']
    )
    return redirect('/', 302)


@app.route('/oidc/logout')
def process_logout():
    logger.info('completed logout')
    return redirect('/', 302)


if __name__ == '__main__':
    app.run()
