import os
from flask import Flask, render_template, request, redirect, url_for, session, flash

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

template_dir = os.path.join(project_root, 'templates')
static_dir = os.path.join(project_root, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = 'supersecretkey'

USER = {'username': 'demo', 'password': 'password123'}

@app.route('/')
def home():
    if 'user' in session:
        return f"<h2>Welcome, {session['user']}!</h2><a href='/logout'>Logout</a>"
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == USER['username'] and password == USER['password']:
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run()

