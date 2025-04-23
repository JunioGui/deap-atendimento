from flask import Flask, render_template_string, request, redirect, url_for, jsonify, send_file
import sqlite3
from datetime import datetime
import pandas as pd

app = Flask(__name__)

# Configurar banco de dados
def init_db():
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_atendido TEXT,
            nome_atendente TEXT,
            nota INTEGER,
            comentario TEXT,
            data_hora TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Página do formulário com visual moderno
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome_atendido = request.form.get('nome_atendido')
        nome_atendente = request.form.get('nome_atendente')
        nota = int(request.form.get('nota'))
        comentario = request.form.get('comentario')
        data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect('feedback.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO feedback (nome_atendido, nome_atendente, nota, comentario, data_hora)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome_atendido, nome_atendente, nota, comentario, data_hora))
        conn.commit()
        conn.close()

        return redirect(url_for('confirmacao'))

    form_html = '''
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Avaliação de Atendimento</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f4f8; margin: 0; padding: 0; }
            header { background: #003366; color: white; padding: 1rem; text-align: center; font-size: 1.5rem; }
            .container { display: flex; justify-content: center; align-items: center; height: 80vh; }
            form { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); width: 300px; }
            input, select, textarea { width: 100%; padding: 0.5rem; margin: 0.5rem 0; border: 1px solid #ccc; border-radius: 8px; }
            button { background: #00509e; color: white; border: none; padding: 0.75rem; border-radius: 8px; width: 100%; cursor: pointer; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
            button:hover { background: #003f7f; }
            footer { background: #003366; color: white; text-align: center; padding: 0.75rem; position: fixed; bottom: 0; width: 100%; font-size: 0.9rem; }
            label i { margin-right: 5px; }
        </style>
        <script src="https://kit.fontawesome.com/a076d05399.js" crossorigin="anonymous"></script>
    </head>
    <body>
        <header>Departamento de Atendimento ao Público - Deap</header>
        <div class="container">
            <form method="post">
                <label><i class="fas fa-user"></i> Nome (opcional):</label>
                <input type="text" name="nome_atendido">
                <label><i class="fas fa-id-badge"></i> Nome do atendente:</label>
                <input type="text" name="nome_atendente" required>
                <label><i class="fas fa-star"></i> Nota (1 a 5):</label>
                <select name="nota" required>
                    <option value="1">1 - Ruim</option>
                    <option value="2">2 - Regular</option>
                    <option value="3">3 - Bom</option>
                    <option value="4">4 - Muito Bom</option>
                    <option value="5">5 - Excelente</option>
                </select>
                <label><i class="fas fa-comment"></i> Comentário:</label>
                <textarea name="comentario" rows="4"></textarea>
                <button type="submit"><i class="fas fa-paper-plane"></i> Enviar</button>
            </form>
        </div>
        <footer>Contato via WhatsApp: (61) 2102-3754</footer>
    </body>
    </html>
    '''
    return render_template_string(form_html)

@app.route('/confirmacao')
def confirmacao():
    return "<h2>Obrigado pelo seu feedback!</h2><a href='/'>Voltar</a>"

if __name__ == '_main_':
    init_db()
    app.run(host='0.0.0.0', port=3000)