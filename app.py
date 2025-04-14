from flask import Flask, request, redirect, url_for, render_template, session
import requests
import json
from google.oauth2 import id_token
from google.auth.transport import requests as grequests

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # change this!

GOOGLE_CLIENT_ID = "1012153519810-tfgdl0r8of4knf35hrces4p5sksmkqsj.apps.googleusercontent.com"


@app.route('/')
def index():
    user = session.get('user')
    return render_template('index.html', user=user)


@app.route('/callback', methods=['GET', 'POST'])
def callback():
    print("Request method:", request.method)
    if request.method == 'POST':
        token = request.form.get('credential')  # For POST method
    else:
        token = request.args.get('credential')  # For GET method

    if not token:
        return "No token found", 400

    try:
        idinfo = id_token.verify_oauth2_token(token, grequests.Request(), GOOGLE_CLIENT_ID)
        session['user'] = {
            'name': idinfo.get('name'),
            'email': idinfo.get('email'),
            'picture': idinfo.get('picture')
        }
    except ValueError:
        return "Invalid token", 400

    return redirect(url_for('index'))




@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
