import email
from operator import or_
from app import app
from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.tables import Cliente
from app.__init__ import db


@app.route('/login', methods=['GET','POST'])
def login():
    #USUÁRIO REQUISITA O ACESSO A SUA CONTA AO PREENCHER O FORMULÁRIO E ENVIAR(BOTÃO ENTRAR)
    if request.method == 'POST': 
        #print(user.email, user.senha, user.id_cliente, user)
        usuario = request.form['username']
        senha = request.form['senha']
        user = Cliente.query.filter_by(email=usuario).first()
        #print(user)
        #CASO NÃO ACHE USUÁRIO OU A SENHA NÃO BATA COM A REGISTRADA DÁ LOGIN INVÁLIDO
        if not user:
            flash('Login Inválido')
        else:
            if not user or not check_password_hash(user.senha, senha):
                flash('Senha incorreta.')
                return redirect(url_for('login'))
            else:
                #LOGA O USUÁRIO E O REDIRECIONA PARA A PÁGINA INICIAL
                login_user(user)
                return redirect(url_for('index'))
    #GET QUE SERIA O USUÁRIO ENTRAR NA PÁGINA DE LOGIN
    return render_template('/login.html')


@app.route('/logout')
def logout():
    #VERIFICA SE HÁ USUÁRIO LOGADO E O DESLOGA SE TIVER
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('index'))

@app.route('/registrar', methods=['GET', 'POST'])
def registra():
    #USUÁRIO PREENCHE FORMULÁRIO E ENVIA PARA A REDDITUS CRIAR UMA NOVA CONTA COM OS DADOS INFORMADOS
    if request.method == 'POST':
        wUser = request.form['rUsuario']
        wSobrenome = request.form['rSobrenome']
        wCpf_Cnpj = request.form['rcpf_cnpj']
        wCnh = request.form['rcnh']
        wdt_nasc = request.form['rdt_nasc']
        wPw = request.form['rPw']
        wEmail = request.form['rEmail']
        #print(request.form)

        #REGISTRA NO BANCO DE DADOS OS DADOS DO CLIENTE E FAZ A CRIPTOGRAFIA(BÁSICÃO) DA SENHA DELE
        usuario = Cliente(nome_cliente=wUser+' '+wSobrenome, cpf_cnpj=wCpf_Cnpj, cnh=wCnh, dt_nasc=wdt_nasc, email=wEmail, senha=generate_password_hash(wPw, method='sha256'))
        db.session.add(usuario)#ADICIONA NO BD
        db.session.commit()#COMMITA A AÇÃO

        return redirect('/login')#REDIRECIONA O USUÁRIO PARA PÁGINA DE LOGIN

    return render_template('registro.html')

#DELETAR CONTA NÃO ESTÁ FUNCIONANDO AINDA
@app.route('/deletar_conta/<id_usuario>')
def deletarConta(id_usuario):
    db.session.delete(Cliente).where(Cliente.id_cliente == id_usuario)
    db.session.commit()