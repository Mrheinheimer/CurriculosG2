from flask import Flask, render_template, request, redirect, url_for, flash, abort
from markupsafe import Markup
import sqlite3
import os
from urllib.parse import urlparse

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'troque-essa-chave-em-producao')
DATABASE = os.environ.get('DATABASE_PATH', 'curriculos.db')


def conectar_banco():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def criar_banco():
    with conectar_banco() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS curriculos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT,
                email TEXT NOT NULL,
                endereco_web TEXT,
                experiencia TEXT NOT NULL
            )
        ''')
        conn.commit()


def validar_url(url):
    if not url:
        return True
    partes = urlparse(url)
    return partes.scheme in ('http', 'https') and bool(partes.netloc)


@app.route('/')
def listar():
    # Proteção contra SQL Injection: não concatena entrada do usuário em SQL.
    with conectar_banco() as conn:
        curriculos = conn.execute(
            'SELECT id, nome, email FROM curriculos ORDER BY id DESC'
        ).fetchall()
    return render_template('listar.html', curriculos=curriculos)


@app.route('/novo', methods=['GET', 'POST'])
def novo():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        telefone = request.form.get('telefone', '').strip()
        email = request.form.get('email', '').strip()
        endereco_web = request.form.get('endereco_web', '').strip()
        experiencia = request.form.get('experiencia', '').strip()

        if not nome or not email or not experiencia:
            flash('Nome, e-mail e experiência profissional são obrigatórios.', 'erro')
            return render_template('novo.html', dados=request.form)

        if endereco_web and not validar_url(endereco_web):
            flash('O endereço WEB deve começar com http:// ou https:// e ser válido.', 'erro')
            return render_template('novo.html', dados=request.form)

        with conectar_banco() as conn:
            # Proteção contra SQL Injection: usa parâmetros (?) em vez de concatenar strings.
            conn.execute(
                '''INSERT INTO curriculos
                   (nome, telefone, email, endereco_web, experiencia)
                   VALUES (?, ?, ?, ?, ?)''',
                (nome, telefone, email, endereco_web, experiencia)
            )
            conn.commit()

        flash('Currículo cadastrado com sucesso.', 'sucesso')
        return redirect(url_for('listar'))

    return render_template('novo.html', dados={})


@app.route('/curriculo/<int:id>')
def consultar(id):
    with conectar_banco() as conn:
        curriculo = conn.execute(
            'SELECT * FROM curriculos WHERE id = ?',
            (id,)
        ).fetchone()

    if curriculo is None:
        abort(404)

    return render_template('consultar.html', curriculo=curriculo)


@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404


@app.after_request
def aplicar_cabecalhos_seguranca(response):
    # Proteção contra XSS e clickjacking/histórico em navegadores.
    response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self'; script-src 'none'; base-uri 'self'; frame-ancestors 'none'"
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    return response


if __name__ == '__main__':
    criar_banco()
    app.run(debug=True)
else:
    criar_banco()
