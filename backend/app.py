from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv
import logging

# Carrega as variáveis de ambiente do .env
load_dotenv()

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

# Configuração do Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(app)

# Verifica se as variáveis de ambiente foram configuradas
if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
    app.logger.error("As credenciais de e-mail não foram configuradas!")
    raise ValueError("As credenciais de e-mail não foram configuradas!")

@app.route('/enviar', methods=['POST'])
def enviar_email():
    data = request.form
    nome = data.get('nome')
    email = data.get('email')
    mensagem = data.get('mensagem')

    if not nome or not email or not mensagem:
        app.logger.warning("Dados do formulário incompletos.")
        return jsonify({'success': False, 'message': 'Por favor, preencha todos os campos do formulário.'}), 400

    msg = Message(
        subject=f"Mensagem de {nome}",
        sender=app.config['MAIL_USERNAME'],
        recipients=[app.config['MAIL_USERNAME']],
        body=f"""
        Nome: {nome}
        E-mail: {email}
        Mensagem: {mensagem}
        """
    )

    try:
        mail.send(msg)
        app.logger.info("E-mail enviado com sucesso!")
        return jsonify({'success': True, 'message': 'E-mail enviado com sucesso!'}), 200
    except Exception as e:
        app.logger.error(f"Erro ao enviar e-mail: {str(e)}")
        return jsonify({'success': False, 'message': f'Erro ao enviar e-mail: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
