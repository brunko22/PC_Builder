import os

import flask
from flask import Flask, request, render_template, redirect, url_for,flash
from flask_caching import Cache
from oauthlib import oauth2
import json
import requests
import Operazioni
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
config = {
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app.config.from_mapping(config)
cache = Cache(app)

DATA = {
    'response_type': "code",
    'redirect_uri': "http://localhost:5000/home",
    'scope': 'https://www.googleapis.com/auth/userinfo.email',
    'client_id': '236858235198-hnss2s640nqeaov59lh840rf8m765i75.apps.googleusercontent.com',
    'prompt': 'consent'}

URL_DICT = {
    'google_oauth': 'https://accounts.google.com/o/oauth2/v2/auth',
    'token_gen': 'https://oauth2.googleapis.com/token',
    'get_user_info': 'https://www.googleapis.com/oauth2/v3/userinfo'
}

# Create a Sign in URI
CLIENT = oauth2.WebApplicationClient('236858235198-hnss2s640nqeaov59lh840rf8m765i75.apps.googleusercontent.com')
REQ_URI = CLIENT.prepare_request_uri(
    uri=URL_DICT['google_oauth'],
    redirect_uri=DATA['redirect_uri'],
    scope=DATA['scope'],
    prompt=DATA['prompt'])


@app.route('/admin')
def admin():
    builds = Operazioni.operation.ricercaAll()
    email = request.cookies.get('email')
    if email is not None:
        user = Operazioni.operation.ricerca_user(email)
        if user is not None and user.get_admin() is True:
            return render_template("admin.html", email=email, builds=builds)
    return redirect("/ricerca")


@app.route('/login')
def login():
    "Home"
    # redirect to the newly created Sign-In URI
    email = request.cookies.get('email')
    if email is None:
        return redirect(REQ_URI)
    return redirect("/admin")

@app.route('/logout')
def logout():
    redirected = redirect(url_for("index"))
    redirected.set_cookie('email', "",0)
    flash("Logout")
    return redirected


@app.route('/home')
def home():
    "Redirect after Google login & consent"

    # Get the code after authenticating from the URL
    code = request.args.get('code')

    # Generate URL to generate token
    token_url, headers, body = CLIENT.prepare_token_request(
        URL_DICT['token_gen'],
        authorisation_response=request.url,
        # request.base_url is same as DATA['redirect_uri']
        redirect_url=request.base_url,
        code=code)

    # Generate token to access Google API
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=('236858235198-hnss2s640nqeaov59lh840rf8m765i75.apps.googleusercontent.com',
              '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'))

    # Parse the token response
    CLIENT.parse_request_body_response(json.dumps(token_response.json()))

    # Add token to the  Google endpoint to get the user info
    # oauthlib uses the token parsed in the previous step
    uri, headers, body = CLIENT.add_token(URL_DICT['get_user_info'])

    # Get the user info
    response_user_info = requests.get(uri, headers=headers, data=body)
    info = response_user_info.json()
    redirected = redirect(url_for("admin"))
    user = Operazioni.operation.ricerca_user((info['email']))
    if user is not None and user.get_admin():
        redirected.set_cookie('email', info['email'], 60)
    return redirected


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context='adhoc')


@app.route('/')
def index():
    email = request.cookies.get('email')
    if email is not None:
        return render_template('index.html', email=email)
    return render_template('index.html')


@app.route('/ricerca')
def ricerca():
    email = request.cookies.get('email')
    if email is not None:
        return render_template('ricerca.html',email=email)
    return render_template('ricerca.html')


@app.route('/insert', methods=['POST'])
def handle_insert():
    email = request.cookies.get('email')
    if email is not None:
        if request.method == 'POST':
            utilizzo = request.form.get('utilizzo')
            fascia = request.form.get('fascia')
            componenti = request.form.get('componenti')
            prezzo = request.form.get('prezzo')
            tipo_ram = request.form.get('tipo_ram')
            Operazioni.operation.insert_build(prezzo, tipo_ram, fascia, utilizzo, componenti)
            flash("Aggiunto")
            return redirect("/admin")
    return redirect('/login')


@app.route('/risultati', methods=['POST'])
def handle_post():
    email = request.cookies.get('email')
    if request.method == 'POST':
        utilizzo = request.form.get('utilizzo')  # Accedi ai dati inviati nel corpo della richiesta POST
        tipo_ram = request.form.get('tipo_ram')
        fascia = request.form.get('fascia')
        builds = Operazioni.operation.ricerca(utilizzo,tipo_ram,fascia)
        if email is not None:
            return render_template("risultati.html", builds=builds, email=email)
        return render_template("risultati.html", builds=builds)


@app.route('/modifica/<uid>')
def modifica(uid):
    email = request.cookies.get('email')
    if email is not None:
        build = Operazioni.operation.ricercaUid(uid)[0]
        return render_template("modifica.html", build=build, email=email)
    return redirect("/login")


@app.route('/update', methods=['POST'])
def update():
    email = request.cookies.get('email')
    if email is not None:
        if request.method == 'POST':
            uid = (request.form.get("uid"))
            prezzo = (request.form.get("prezzo"))
            fascia = (request.form.get("fascia"))
            componenti = (request.form.get("componenti"))
            utilizzo = (request.form.get("utilizzo"))
            tipo_ram = (request.form.get("tipo_ram"))
            Operazioni.operation.update(uid, prezzo, fascia, componenti, utilizzo, tipo_ram)
            flash("Modificato")
        return redirect("/admin")
    return redirect("/login")


@app.route('/cancella', methods=['POST'])
def cancella():
    email = request.cookies.get('email')
    if email is not None:
        if request.method == 'POST':
            uid = request.form.get("uid")
            Operazioni.operation.delete(uid)
            flash("Eliminato")
        return redirect("/admin")
    return redirect("/login")


if __name__ == '__main__':
    app.run(ssl_context='adhoc')
