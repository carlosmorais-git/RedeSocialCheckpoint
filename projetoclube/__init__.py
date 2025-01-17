# # **********ARQUIVO DE INICIALIZAÇÃO DO MEU PROJETO**********

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import sqlalchemy
import logging


# Configuração de logs
'''
Controle de Nível : Permite categorizar mensagens por gravidade, como:

DEBUG: Para mensagens enviadas, usadas durante o desenvolvimento.
INFO: Para mensagens informativas, como notificações de que algo foi concluído com sucesso.
WARNING: Para avisos de possíveis problemas.
ERROR: Para erros que impedem a execução de uma funcionalidade.
CRITICAL: Para falhas graves que comprometem a aplicação.

'''
logging.basicConfig(level=logging.INFO) # Define o nível de detalhe (INFO e superiores)
logger = logging.getLogger(__name__) # Cria um logger específico para o módulo atual


# Inicializando o aplicativo Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'aa749d5659aa92382d79c177cdb4445e057b2184'

# Configuração do banco de dados
if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # Banco de dados no servidor
    logger.info("Banco de dados configurado para produção.")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bancoDB.db'  # Banco de dados local
    logger.info("Banco de dados configurado para desenvolvimento local.")


# Inicializando extensões
database = SQLAlchemy(app)  # Instância do banco de dados
bcrypt = Bcrypt(app)  # Criptografia
login_manager = LoginManager(app)  # Gerenciamento de login


# Caso o usuario tente acessar uma pagina que só quem permissao for usuario
# redireciona para a pagina de login
login_manager.login_view = 'login'

# modifica o estilo da mensagem
login_manager.login_message = 'Entre em uma conta primeiro! Para prosseguir.'
login_manager.login_message_category = 'alert-warning'


# Função para verificar e inicializar o banco de dados
def verificar_banco():
    engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sqlalchemy.inspect(engine)

    # Verifica se a tabela "usuario" existe
    if not inspector.has_table("usuario"):
        with app.app_context():
            database.create_all()
            logger.info("Banco de dados criado com as tabelas necessárias.")
    else:
        logger.info("Banco de dados já existe.")

# Executa a verificação do banco de dados
verificar_banco()

# Importando rotas e modelos
from projetoclube import models
from projetoclube import routes

