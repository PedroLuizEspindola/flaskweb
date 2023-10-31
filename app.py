from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Configuração do banco de dados SQLite
DATABASE_RESERVAS = 'reservas.db'
DATABASE_CONTATOS = 'contatos.db'

def create_tables():
    # Criação da tabela para reservas
    conn_reservas = sqlite3.connect(DATABASE_RESERVAS)
    cur_reservas = conn_reservas.cursor()
    cur_reservas.execute('''CREATE TABLE IF NOT EXISTS reservas (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            telefone TEXT NOT NULL,
                            horario TEXT NOT NULL,
                            data TEXT NOT NULL,
                            num_pessoas INTEGER NOT NULL,
                            comentario TEXT
                        )''')
    conn_reservas.commit()
    conn_reservas.close()

    # Criação da tabela para contatos
    conn_contatos = sqlite3.connect(DATABASE_CONTATOS)
    cur_contatos = conn_contatos.cursor()
    cur_contatos.execute('''CREATE TABLE IF NOT EXISTS contatos (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            email TEXT NOT NULL,
                            mensagem TEXT NOT NULL
                        )''')
    conn_contatos.commit()
    conn_contatos.close()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def contatos():
    if request.method == 'POST':
        # Lógica para inserir dados na tabela de contatos
        nome = request.form['name']
        email = request.form['email']
        mensagem = request.form['message']

        conn = sqlite3.connect(DATABASE_CONTATOS)
        cur = conn.cursor()
        cur.execute('''INSERT INTO contatos (nome, email, mensagem)
                       VALUES (?, ?, ?)''', (nome, email, mensagem))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/index' , methods=['GET', 'POST'])
def start():
    return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reservation')
def reservation():
    return render_template('reservation.html')

@app.route('/reservation', methods=['POST'])
def reservas():
    if request.method == 'POST':
        nome = request.form['booking-form-name']
        telefone = request.form['booking-form-phone']
        horario = request.form['booking-form-time']
        data = request.form['booking-form-date']
        num_pessoas = request.form['booking-form-number']
        comentario = request.form['booking-form-message']
        
        conn = sqlite3.connect(DATABASE_RESERVAS)
        cur = conn.cursor()
        cur.execute('''INSERT INTO reservas (nome, telefone, horario, data, num_pessoas, comentario)
                       VALUES (?, ?, ?, ?, ?, ?)''', (nome, telefone, horario, data, num_pessoas, comentario))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
