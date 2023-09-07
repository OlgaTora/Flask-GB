from flask import Flask, render_template, request, redirect, url_for, make_response, session, flash
from utils import is_mail

app = Flask(__name__)
"""
>>> import secrets
>>> print(secrets.token_hex())
"""

app.secret_key = '8f1e4cde6804c8b204b3d7b903f1d24d58a97994ea0b0d60cc5be23dd524f26d'


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('hello', username=f'{session["username"]}'))
    else:
        return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    context = {'page': 'login'}
    if request.method == 'POST':
        session['username'] = request.form.get('username') or 'NoName'
        mail = request.form.get('mail')
        if not is_mail(mail):
            flash('Wrong name or email! Try again', 'danger')
        else:
            username = request.form.get('username')
            return redirect(url_for('hello', username=username))
    return render_template('login.html', **context)


@app.route('/hello/<string:username>', methods=['GET', 'POST'])
def hello(username):
    response = make_response(render_template('hello.html', username=username))
    response.headers['new_head'] = 'New value'
    response.set_cookie('username', username)
    return response


@app.route('/logout/')
def logout():
    session.clear()
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('username')
    return response
