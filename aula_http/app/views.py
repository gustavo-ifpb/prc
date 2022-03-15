from flask import Flask

from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, redirect, url_for, session, make_response

from app import app

auth = HTTPBasicAuth()

users = {
    "fulano": generate_password_hash("opa"),
    "cicrano": generate_password_hash("eita")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/')
def index():
    name = request.cookies.get('name')
    if not name:
        name = 'Nenhum nome informado!'
    return render_template('index.html', name=name)

@app.route('/setCookie', methods=['POST'])
def setCookie():
    name = request.form['name']
    
    resp = make_response( redirect( url_for('index') ) )
    resp.set_cookie('name', name)

    return resp

@app.route('/clearCookie')
def clearCookie():
    resp = make_response( redirect( url_for('index') ) )
    resp.set_cookie('name', '', expires=0)

    return resp

@app.route('/secretPage')
@auth.login_required
def basicSecretPage():
    return render_template('secret.html')