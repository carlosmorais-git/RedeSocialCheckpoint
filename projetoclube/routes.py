# **********ARQUIVO DE CRIAÇÃO PARA ROTAS DAS PAGINAS**********

from flask import render_template,url_for,flash,redirect,request,abort
from projetoclube import app,database,bcrypt
from projetoclube.forms import CriarFormulario_criarConta,CriarFormulario_login,CriarFormulario_post
from projetoclube.models import Usuario,Post
from flask_login import login_user,logout_user,current_user,login_required
import secrets
import os
from PIL import Image



# render_template - renderiza uma pagina html para uma rota
# url_for - permite que recupero url das funcoes de maneira dinamica em vez de escreve elas assim '/caminho'
# flash - mensagem de alerta
# redirect - redirecionar para uma pagina
# login_user - loga o usuario no site
# bcrypt - usa quando for criptrografar uma senha
# logout_user - deslogar usuario
# current_user - verfica se o usuario esta autenticado e controla a exibição dele na pagina
# request - faz requisição na url da pagina
# login_required - bloqueia a pagina caso caso usuario não esta logado



# Decoretor (route) é uma funcao que atribui uma nova funcionalidade 
# para a funcao de baixo

# -------Pagina Principal-------
@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    form = CriarFormulario_post()
    return render_template('home.html',
                           titulo='Bem Vindo ao Clube Do Jogo',
                           subtitulo='Veja o que estão falando do assunto do dia',
                           posts=posts,
                           form=form,
                           botao_submit_criar_post='Criar Post')


# -------Pagina Contatos salvos-------
@app.route('/suporte')
@login_required# bloqueia a pagina caso nao faço login
def suporte():
    return render_template('suporte.html',titulo='Suporte da Empresa')


# -------Pagina Usuarios-------
@app.route('/usuarios')
@login_required# bloqueia a pagina caso nao faço login
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html',
                           titulo='Campo do Usuario', 
                           subtitulo = 'Lista de Contas Gamer:',
                           lista_usuarios = lista_usuarios) # passando uma variavel do python para o html


# -------Pagina Logar no site-------
# Paginas que tem algum formulario interno, preciso liberar o metodo POST passando o parametro methods
@app.route('/login', methods=['GET','POST'])
def login():

    form_login = CriarFormulario_login()

    if form_login.validate_on_submit():
        # exibindo um alerta com o email logado usando .data
        # usando .data recupero o que o usuario escreveu no input

        # Verificando se esse usuario existe
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()

        # Caso o Usuario existir e senha for a salva, consiguirar logar
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            # Logar o usuario e verificar de precisa salvar seus dados de acesso
            login_user(usuario, remember=form_login.lembrar_dados.data)

            flash(message='Login feito com sucesso! Bem-Vindo {}'.format(str(usuario.nome_usuario).title()),
                category='alert-success')
            parametro_next = request.args.get('next')
            if parametro_next:
                # redireciona para um link '/'
                return redirect(parametro_next)       
            else:
                return redirect(url_for('home'))
        
        else:
            flash(message='Falha no Login, E-mail ou Senha Incorretos',
                category='alert-danger')
            

    return render_template('tela_login.html',form_login = form_login)



# -------Pagina Criar um novo usuario-------
@app.route('/criar-conta', methods=['GET','POST'])
def criarConta():

    form_criar_conta = CriarFormulario_criarConta()
    if form_criar_conta.validate_on_submit():
        # criptrografando o senha do usuario
        senha_criptrografada = bcrypt.generate_password_hash(form_criar_conta.senha.data).decode('utf-8')

        # criar um usuario - nome,email,senha
        usuario = Usuario(nome_usuario = form_criar_conta.usuario.data, 
                          email = form_criar_conta.email.data, 
                          senha = senha_criptrografada)
        
        # abrir um sessao para adicionar o usuario
        database.session.add(usuario)
        # salvar edicao no banco de dados
        database.session.commit()


        flash(message='Conta criada com sucesso! O E-mail {} está liberado para logar.'.format(form_criar_conta.email.data),
              category='alert-success')
        
        # Redirecionar para uma pagina especifica
        return redirect(url_for('login'))
    
    return render_template('tela_criarConta.html',form_criar_conta = form_criar_conta)



# -------Deslogar da conta logada-------
@app.route('/sair')
@login_required# bloqueia a pagina caso nao faço login
def sair():

    # Deslogar um usuario
    logout_user()
    flash(message='Você acabou de sair de uma conta do Clube! \nVolte para continuar compartilhando experiências.',
                category='alert-info')
    return redirect(url_for('login'))


# -------Pagina Perfil do usuario-------
@app.route('/perfil')
@login_required# bloqueia a pagina caso nao faço login
def perfil():
    #Filtrando os posts so pelo usuario logado e reorganizando por posts mais novos
    posts = Post.query.filter_by(id_usuario=current_user.id).order_by(Post.id.desc()).all()
       
   
    foto_perfil = url_for('static',filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html',titulo = 'Historias Compartilhadas', foto_perfil = foto_perfil,posts=posts)


# -------Pagina Criar um post-------
@app.route('/', methods=['GET','POST'])
@login_required# bloqueia a pagina caso nao faço login
def criar_post():
    form = CriarFormulario_post()

    if form.validate_on_submit():

        # Criando a instancia do post
        post = Post(titulo=form.titulo.data,  # Passando o titulo do post criado no formulario
                    corpo=form.corpo.data,    # Passando o corpo do conteudo
                    autor=current_user)                  # Dizendo que o autor é o usuario logado
        database.session.add(post)
        database.session.commit()
        flash(message='Post criado com sucesso!', category='alert-success')
        return redirect(url_for('home'))

    return render_template('home.html',form=form,botao_submit_criar_post='Criar Post')





# -------Pagina Editar usuario-------
# Variável para controlar o modo de edição
edit_mode = {"nome_usuario": False, "email": False, "bio": False, 'foto_perfil': False}
erro_encontrado = False

# Função para salvar imagem no servidor
def salvar_imagem(imagem):
    # Pegar o local onde irá salvar a imagem
    nome, extensao = os.path.splitext(imagem.filename)

    # Adicionar um código único ao nome da imagem
    codigo = secrets.token_hex(8)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)

    # Reduzir o tamanho da imagem
    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)  # Ler a imagem
    imagem_reduzida.thumbnail(tamanho)  # Reduzir o tamanho
    imagem_reduzida.save(caminho_completo)  # Salvar imagem reduzida

    return nome_arquivo

# Página Editar Perfil
@app.route('/perfil/editar', methods=["GET", "POST"])
@login_required  # Bloqueia a página caso o usuário não esteja logado
def editar_perfil():

    global edit_mode, erro_encontrado

    if request.method == "POST":
        field = request.form.get("field")  # Pagina selecionada pra edicao
        value = request.form.get("value")  # valores passado no formulario
        foto = request.files.get("foto_perfil")  # foto selecionada pelo usuario
    
        if field:
            # Lógica para editar o campo nome, email ou bio
            if field == "email" and current_user.email != value:

                # Verifica se existe no banco de dados
                email_existente = Usuario.query.filter_by(email=value).first()
                if email_existente:
                    flash(f'E-mail {value} já cadastrado.', category='alert-danger')
                    # o erro encontrado controla a exibicao de erro do formulario email
                    erro_encontrado = True

                elif value:
                    setattr(current_user, field, value)  # Atualiza dinamicamente o campo
                    database.session.commit()
                    edit_mode[field] = False# fecha o modo edicao
                    return redirect(url_for('editar_perfil'))
                
            elif field == "foto_perfil" and foto:

                # Salvar a nova foto de perfil
                if str(foto.filename).lower()[-4:] in ['.jpg','.png']:
                    nome_arquivo = salvar_imagem(foto)
                    current_user.foto_perfil = nome_arquivo
                    database.session.commit()
                    edit_mode[field] = False# fecha o modo edicao
                    return redirect(url_for('editar_perfil'))
                else:
                    flash(f'Formato de foto não permitida! Tente um formato válido PNG ou JPG.', category='alert-danger')
                    return redirect(url_for('editar_perfil'))
            
            else:
                setattr(current_user, field, value)
                database.session.commit()                
                edit_mode[field] = False# fecha o modo edicao
                return redirect(url_for('editar_perfil'))

    # Caminho da foto de perfil
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('editar_perfil.html',
                           erro_encontrado=erro_encontrado,
                           edit_mode=edit_mode,
                           foto_perfil=foto_perfil,
                           titulo='Modo Editor')

# Ativar modo de edição -  Crio uma pagina dinamica para cada item passado no < field >
@app.route("/edit/<field>")
@login_required  # Bloqueia a página caso o usuário não esteja logado
def edit(field):
    global edit_mode

    if field in edit_mode:
        edit_mode[field] = True  # Ativa o modo de edição para o campo
    
    return redirect(url_for("editar_perfil"))

# Ativar modo de edição -  Crio uma pagina dinamica para cada item passado no < field >
@app.route("/reset/<field>")
@login_required  # Bloqueia a página caso o usuário não esteja logado
def reset(field):
    global edit_mode

    if field:
        if field == 'resetar':
            for chave in edit_mode:
                edit_mode[chave] = False  # Desativar todos os campos
        else:
            edit_mode[field] = False # Desativa um campo por vez
            return redirect(url_for("editar_perfil"))
    
    return redirect(url_for("perfil"))


@app.route("/teste")
def teste():
    return render_template('teste.html')

# Função que cria uma pagina para cada post criado
# assim pego o mesmo 
@app.route("/post/<field>", methods=["GET", "POST"])
@login_required  # Bloqueia a página caso o usuário não esteja logado
def exibir_post(field):

    post = Post.query.get(field)
    if current_user == post.autor:

        form = CriarFormulario_post()

        if request.method == 'GET':

            # Preencher automatico assim que carregar a pagina
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo

        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post Atualizado comSucesso', category='alert-success')
            return redirect(url_for("home"))
    else:
        form=None 

    return render_template('post.html',post=post,form=form,titulo='Editar Post',botao_submit_criar_post='Editar Post')


@app.route("/post/<field>/excluir", methods=["GET", "POST"])
@login_required  # Bloqueia a página caso o usuário não esteja logado
def excluir_post(field):

    post = Post.query.get(field)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluido', category='alert-danger')
        return redirect(url_for("home"))
    else:
        abort(403)
