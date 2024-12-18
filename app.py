from flask import Flask, request, render_template, \
    redirect, url_for, flash
import sqlite3, os.path

DATABASE = 'database.db'

app = Flask(__name__)

# habilitar mensagens flash
app.config['SECRET_KEY'] = 'muitodificil'

# obtém conexão com o banco de dados
def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET','POST'])
def login():
    texto = ''
    if request.method=='POST':
        email = request.form['email']
        senha = request.form['password']
        conn = get_connection()
        users = conn.execute("SELECT * FROM users").fetchall()
        conn.close()
        
        for user in users:
            if email in user and senha in user:
                return render_template('dashboard.html')
            else:
                texto = 'Email ou Senha incorreta. Tente novamente!'
    return render_template('login.html', texto=texto)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        senha= request.form['password']

        if not email:
            flash('Email é obrigatório')
        else:
            conn = get_connection()
            conn.execute("INSERT INTO users(email, senha) VALUES (?,?)", (email, senha))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
    
    return render_template('register.html')