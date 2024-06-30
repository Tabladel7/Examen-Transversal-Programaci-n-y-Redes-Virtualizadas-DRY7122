import pyotp
import sqlite3
import hashlib
import uuid
import os
from flask import Flask, request

app = Flask(__name__)

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
db_name = os.path.join(desktop_path, 'usuarios y contraseñas.db')

@app.route('/')
def index():
    return 'Sitio web de gestión de credenciales.'
@app.route('/signup/v1', methods=['POST'])
def signup_v1():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS USER_PLAIN (
            USERNAME TEXT PRIMARY KEY NOT NULL,
            PASSWORD TEXT NOT NULL
        );
    ''')
    conn.commit()
    try:
        c.execute('''
            INSERT INTO USER_PLAIN (USERNAME, PASSWORD)
            VALUES (?, ?)
        ''', (request.form['username'], request.form['password']))
        conn.commit()
    except sqlite3.IntegrityError:
        return "El usuario ya ha sido registrado"
    finally:
        conn.close()
    
    return "Registro exitoso"

def verify_plain(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    query = "SELECT PASSWORD FROM USER_PLAIN WHERE USERNAME = ?"
    c.execute(query, (username,))
    record = c.fetchone()
    conn.close()
    if not record:
        return False
    return record[0] == password

@app.route('/login/v1', methods=['GET', 'POST'])
def login_v1():
    error = None
    if request.method == 'POST':
        if verify_plain(request.form['username'], request.form['password']):
            error = 'Inicio de sesión exitoso'
        else:
            error = 'Usuario/contraseña inválidos'
    else:
        error = 'Método no válido'
    return error

@app.route('/signup/v2', methods=['GET', 'POST'])
def signup_v2():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS USER_HASH (
            USERNAME TEXT PRIMARY KEY NOT NULL,
            HASH TEXT NOT NULL
        );
    ''')
    conn.commit()
    try:
        hash_value = hashlib.sha256(request.form['password'].encode()).hexdigest()
        c.execute('''
            INSERT INTO USER_HASH (USERNAME, HASH)
            VALUES (?, ?)
        ''', (request.form['username'], hash_value))
        conn.commit()
    except sqlite3.IntegrityError:
        return "El usuario ya ha sido registrado"
    finally:
        conn.close()
    
    return "Registro exitoso"

def verify_hash(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    query = "SELECT HASH FROM USER_HASH WHERE USERNAME = ?"
    c.execute(query, (username,))
    record = c.fetchone()
    conn.close()
    if not record:
        return False
    return record[0] == hashlib.sha256(password.encode()).hexdigest()

@app.route('/login/v2', methods=['GET', 'POST'])
def login_v2():
    error = None
    if request.method == 'POST':
        if verify_hash(request.form['username'], request.form['password']):
            error = 'Inicio de sesión exitoso'
        else:
            error = 'Usuario/contraseña inválidos'
    else:
        error = 'Método no válido'
    return error

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5800, ssl_context='adhoc')
