from flask import Flask, render_template_string, request, redirect, url_for, jsonify, send_file
import sqlite3
from datetime import datetime
import pandas as pd
import re

app = Flask(__name__)

# Banco de dados
def init_db():
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_atendido TEXT,
            cpf TEXT,
            email TEXT,
            nome_atendente TEXT,
            nota INTEGER,
            comentario TEXT,
            data_hora TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Página do formulário
@app.route('/', methods=['GET', 'POST'])
def index():
    erro = None
    if request.method == 'POST':
        nome_atendido = request.form.get('nome_atendido')
        cpf = request.form.get('cpf')
        email = request.form.get('email')
        nome_atendente = request.form.get('nome_atendente')
        nota = int(request.form.get('nota'))
        comentario = request.form.get('comentario')

        # Validação CPF e e-mail
        if not cpf or not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
            erro = 'CPF inválido. Use o formato 000.000.000-00.'
        elif not email or not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            erro = 'Formato de e-mail inválido.'

        if not erro:
            data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            conn = sqlite3.connect('feedback.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO feedback (nome_atendido, cpf, email, nome_atendente, nota, comentario, data_hora)
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (nome_atendido, cpf, email, nome_atendente, nota, comentario, data_hora))
            conn.commit()
            conn.close()
            return redirect(url_for('confirmacao'))

    return render_template_string(form_html, erro=erro)

@app.route('/confirmacao')
def confirmacao():
    return "<h2>Obrigado pela sua avaliação!</h2><a href='/'>Voltar</a>"

form_html = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DEAP - Avaliação</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f0f4f8;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
        }
        header {
            width: 100%;
            background-color: #003366;
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
        }
        .logo {
            margin: 20px auto;
            text-align: center;
        }
        .logo img {
            max-width: 200px;
            height: auto;
        }
        .form-container {
            background-color: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            width: 90%;
            max-width: 500px;
            text-align: center;
        }
        input, select, textarea {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border-radius: 10px;
            border: 1px solid #ccc;
            font-size: 16px;
        }
        button {
            background-color: #004c99;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
            box-shadow: 0 3px 6px rgba(0,0,0,0.1);
        }
        button:hover {
            background-color: #003366;
        }
        footer {
            margin-top: 20px;
            font-size: 14px;
            color: #555;
        }
    </style>
</head>
<body>
    <header>Departamento de Atendimento ao Público - Deap</header>

    <div class="logo">
        <img src="https://uploaddeimagens.com.br/images/004/759/503/full/logo-coren-df.png" alt="Logo Coren-DF">
    </div>

    <div class="form-container">
        <h2>Avalie aqui nosso atendimento</h2>
        {% if erro %}<p style="color:red;">{{ erro }}</p>{% endif %}
        <form method="post">
            <input type="text" name="nome_atendido" placeholder="Seu nome (opcional)">
            <input type="text" name="cpf" placeholder="Seu CPF (000.000.000-00)" required>
            <input type="email" name="email" placeholder="Seu e-mail" required>
            <input type="text" name="nome_atendente" placeholder="Nome do atendente" required>
            <select name="nota" required>
                <option value="">Nota (1 a 5)</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
            </select>
            <textarea name="comentario" placeholder="Comentário" rows="4"></textarea>
            <button type="submit">Enviar</button>
        </form>
        <footer>
            <i class="fab fa-whatsapp"></i> (61) 2102-3754
        </footer>
    </div>
</body>
</html>
'''

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=3000)
