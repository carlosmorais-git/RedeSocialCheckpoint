# **********ARQUIVO DE INICIALIZAÇÃO DO MEU PROJETO**********

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import sqlalchemy

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



from projetoclube import models

engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

# esse inspector serve para verificar se uma tabela existe dentro do banco de dados
inspector = sqlalchemy.inspect(engine)

# verifica se o banco de dados já criado nao tem a tabela 'usuario'
if not inspector.has_table("usuario"):
    with app.app_context():
        database.drop_all()
        database.create_all()
        print('Banco de dados criado')
else:
    print('Banco de dados já existe')

# Importando meus links apos a criancao do meu 'app'
from projetoclube import routes
