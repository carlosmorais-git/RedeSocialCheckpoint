# **********ARQUIVO DE INICIALIZAÇÃO DO MEU PROJETO**********

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = 'aa749d5659aa92382d79c177cdb4445e057b2184'

if os.getenv('DATABASE_URL'):
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') # configuracao do banco de dados no servidor

else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clube.db' # configuracao do banco de dados local

database = SQLAlchemy(app)# criando o banco de dados
bcrypt = Bcrypt(app)# usando essa classe so meu site será capaz de criptrografar e descriptrografar
login_manager = LoginManager(app)

# Caso o usuario tente acessar uma pagina que só quem permissao for usuario
# redireciona para a pagina de login
login_manager.login_view = 'login'
# modifica o estilo da mensagem
login_manager.login_message = 'Entre em uma conta primeiro! Para prosseguir.'
login_manager.login_message_category = 'alert-warning'


# Importando meus links apos a criancao do meu 'app'
from projetoclube import routes