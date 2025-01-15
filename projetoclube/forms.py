# ********** ARQUIVO DE CRIAÇÃO DOS FORMULARIOS **********

#  FlaskForm - para criar formulario
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

# wtforms - para importa os campos de inputs
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo ,ValidationError
from projetoclube.models import Usuario
from flask_login import current_user


# DataRequired = Para compos obriatorios
# Length = Definir um tamanho
# Email = Verificar formato de email valido
# EqualTo = É para varificar se os valores dos campos sao iguais

# é presciso passa uma lista de validators=[] de parametros

# Usando o FlaskForm de parametro irei herda seu init por padrao

class CriarFormulario_criarConta(FlaskForm):

    usuario = StringField('Nome de Usuário',validators=[DataRequired()])
    email = StringField('E-mail',validators=[DataRequired(),Email()])
    senha = PasswordField('Senha',validators=[DataRequired(),Length(6,20)])
    confirmacao_senha = PasswordField('Confirmação da Senha',validators=[DataRequired(),EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    # Este método precisa começar com o prefixo 'validate_' para o 'validate_on_submit()' verificar automatico e 
    # funcionar como um validador, pois esse é o padrão sugerido.
    # Ele verifica se o e-mail fornecido já está em uso. 
    # Caso esteja, lança uma exceção utilizando 'raise' da classe 'ValidationError'.
    def validate_email(self, email):
        email_sugerido = Usuario.query.filter_by(email=email.data).first()
        if email_sugerido:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar.')




class CriarFormulario_login(FlaskForm):
    
    email = StringField('E-mail',validators=[DataRequired(),Email()])
    senha = PasswordField('Senha',validators=[DataRequired(),Length(6,20)])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')
    botao_submit_fazerlogin = SubmitField('Fazer Login')


class CriarFormulario_editar_perfil(FlaskForm):
   
    usuario = StringField('Nome de Usuário',validators=[DataRequired()])
    email = StringField('E-mail',validators=[DataRequired(),Email()],name="value")
    foto_perfil = FileField('Atualizar Foto',validators=[FileAllowed(['jpg','png'])])
    botao_submit_editar = SubmitField('Confirmar Edicao')
   
    def validate_editar_conta(self, email):

        if current_user.email != email.data:
            email_sugerido = Usuario.query.filter_by(email=email.data).first()
            if email_sugerido:
                raise ValidationError(f'E-mail {email.data} já cadastrado. Confirma edição para continuar com o seu e-mail antigo.')


class CriarFormulario_post(FlaskForm):

    titulo = StringField('Titulo do Post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu Post Aqui', validators=[DataRequired()])
    botao_submit_criar_post = SubmitField('Criar Post')