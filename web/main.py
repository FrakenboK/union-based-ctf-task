from flask import Flask, request, render_template, redirect, url_for, session
import random, hashlib, time
from database.postgres import Database
from config.config import Config
from datetime import datetime

app = Flask(
    'union-based-ctf-task',
    static_folder='static',
    template_folder='templates'
)

app.secret_key = str(random.randint(1000000,1000000000))
cfg = Config()
db = Database(cfg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('create'))

    if request.method == 'GET':
        if 'error' in request.args:
            return render_template('register.html', error=request.args['error'])
        return render_template('register.html')
    

    username = request.form.get('username')
    password = request.form.get('password')

    if not (0 < len(username) < 100 and 0 < len(password) < 100):
        return redirect(url_for('register', error='Invalid username or password'))

    user = db.get_user(username)
    
    if user is not None:
        return redirect(url_for('register', error='User is already exists'))
        
    db.create_user(username, hashlib.md5(password.encode()).hexdigest())

    return redirect(url_for('login', message='Register succesfull'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('create'))
    
    if request.method == 'GET':
        if 'error' in request.args:
            return render_template('login.html', error=request.args['error'])
        if 'message' in request.args:
            return render_template('login.html', message=request.args['message'])
        return render_template('login.html')
    
    username = request.form.get('username')
    password = request.form.get('password')

    if not (0 < len(username) < 100 and 0 < len(password) < 100):
        return redirect(url_for('login', error='Invalid username or password'))

    user = db.get_user(username)

    if user is None:
        return redirect(url_for('login', error='User doesn\'t exists'))
    
    if user[2] != hashlib.md5(password.encode()).hexdigest():
        return redirect(url_for('login', error='Invalid credentials'))
    
    session['user_id'] = user[0]

    return redirect(url_for('create'))


@app.route('/create',  methods=['GET', 'POST'])
def create():
    if 'user_id' not in session:
        return redirect(url_for('login', error="You are not authorized"))
    
    if request.method == 'GET':
        if 'error' in request.args:
            return render_template('add_note.html', error=request.args['error'])
        return render_template('add_note.html')
    
    title = request.form.get('title')
    message = request.form.get('message')

    if not (title is not None and message is not None and 0 < len(title) < 100 and 0 < len(message) < 100):
        return redirect(url_for('create', error='Invalid notes Info'))
    stamp = int(time.time())
    db.create_note(session['user_id'], title, message, datetime.fromtimestamp(stamp).strftime('%c'))

    return redirect(url_for('notes'))



@app.route('/notes',  methods=['GET'])
def notes():
    if 'user_id' not in session:
        return redirect(url_for('login', error="You are not authorized"))
    
    if "search" in request.args and request.args['search']!='':
        notes = db.search_user_notes(session['user_id'], request.args['search'])
    else:
        notes = db.get_user_notes(session['user_id'])

    return render_template('notes.html', notes=notes)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234, debug=False)