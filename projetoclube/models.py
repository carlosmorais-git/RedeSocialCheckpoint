# **********ARQUIVO DE CRIAÇÃO DOS MODELOS DE BANCO DE DADOS**********

from projetoclube import database, login_manager
from datetime import datetime, timedelta

# O metodo UserMixin permite que o login_manager faça controle do usuario na pagina
from flask_login import UserMixin

# Para dizer ao login_manager que essa funcao
# carregar um usuario, verificando seu id
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

# Criando Tabela de Usuario
class Usuario(database.Model, UserMixin):# subclass
    id = database.Column(database.Integer, primary_key=True)
    nome_usuario = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)

    foto_perfil = database.Column(database.String, default='default.jpg')
    bio = database.Column(database.Text,default='Videogames são portas para mundos infinitos, onde arte, narrativa e tecnologia se encontram.')
    post = database.relationship('Post', backref='autor', lazy=True)
    cursos = database.Column(database.String, nullable=False, default='não informado')

    def contar_posts(self):
        return len(self.post)

# Criando Tabela do Post
class Post(database.Model):# subclass
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text,nullable=False)
    
    # Criando a relacao com o autor do post 
    # Para usar a chave estrangeira preciso passar o nome da classe em minuscula
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'),nullable=False)

    # Passando um metodo padrao de data, toda vez que um post for criado
    data_criacao = database.Column(database.DateTime, nullable=False,default=datetime.now)


    def tempo_relativo(self):
        '''Tem o proposito de retorna uma data de criação do post mais amigavel adaptando no decorrer do tempo'''
        agora = datetime.now()
        diferenca = agora - self.data_criacao

        if diferenca < timedelta(minutes=1):
            return "há poucos segundos"
        elif diferenca < timedelta(hours=1):
            minutos = diferenca.seconds // 60
            return f"há {minutos}m"
        elif diferenca < timedelta(days=1):
            horas = diferenca.seconds // 3600
            return f"há {horas}h"
        elif diferenca < timedelta(days=30):
            dias = diferenca.days
            return f"há {dias}d"
        elif diferenca < timedelta(days=365):
            meses = diferenca.days // 30
            return f"há {meses}m"
        else:
            anos = diferenca.days // 365
            return f"há {anos}a"