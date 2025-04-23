from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3
from datetime import datetime
import re

app = Flask(__name__)

# Banco de dados
def init_db():
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    cursor.execute("""
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
    """)
    conn.commit()
    conn.close()

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

        if not cpf or not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
            erro = 'CPF inválido. Use o formato 000.000.000-00.'
        elif not email or not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            erro = 'Formato de e-mail inválido.'

        if not erro:
            data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            conn = sqlite3.connect('feedback.db')
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO feedback (nome_atendido, cpf, email, nome_atendente, nota, comentario, data_hora)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (nome_atendido, cpf, email, nome_atendente, nota, comentario, data_hora))
            conn.commit()
            conn.close()
            return redirect(url_for('confirmacao'))

    return render_template_string(form_html, erro=erro)

@app.route('/confirmacao')
def confirmacao():
    return "<h2>Obrigado pela sua avaliação!</h2><a href='/'>Voltar</a>"

form_html = """
<!DOCTYPE html>
<html lang='pt-br'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>DEAP - Avaliação</title>
    <link href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css' rel='stylesheet'>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f8fc;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
        }
        header {
            background-color: #003366;
            color: white;
            width: 100%;
            text-align: center;
            padding: 1rem;
            font-size: 1.5rem;
        }
        .logo {
            margin: 1rem 0;
        }
        .logo img {
            max-width: 200px;
        }
        form {
            background: white;
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            width: 90%;
            max-width: 500px;
        }
        input, select, textarea {
            width: 100%;
            padding: 0.75rem;
            margin: 0.5rem 0;
            border: 1px solid #ccc;
            border-radius: 0.75rem;
            font-size: 1rem;
        }
        button {
            background-color: #004aad;
            color: white;
            padding: 0.75rem;
            border: none;
            width: 100%;
            border-radius: 0.75rem;
            font-size: 1rem;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        footer {
            margin-top: 1rem;
            font-size: 0.9rem;
            color: #333;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
    </style>
</head>
<body>
    <header>Departamento de Atendimento ao Público - Deap</header>
    <div class='logo'>
        <img src='https://uploaddeimagens.com.br/images/004/759/503/full/logo-coren-df.png' alt='Logo Coren DF'>
    </div>
    <form method='POST'>
        <h2>Avalie aqui nosso atendimento</h2>
        {% if erro %}<p style='color:red;'>{{ erro }}</p>{% endif %}
        <input type='text' name='nome_atendido' placeholder='Seu nome (opcional)'>
        <input type='text' name='cpf' placeholder='Seu CPF (000.000.000-00)' required>
        <input type='email' name='email' placeholder='Seu e-mail' required>
        <input type='text' name='nome_atendente' placeholder='Nome do atendente' required>
        <select name='nota' required>
            <option value=''>Nota (1 a 5)</option>
            <option value='1'>1</option>
            <option value='2'>2</option>
            <option value='3'>3</option>
            <option value='4'>4</option>
            <option value='5'>5</option>
        </select>
        <textarea name='comentario' placeholder='Comentário'></textarea>
        <button type='submit'>Enviar</button>
    </form>
    <footer>
        <i class='fab fa-whatsapp'></i> (61) 2102-3754
    </footer>
</body>
</html>
"""

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=3000)
