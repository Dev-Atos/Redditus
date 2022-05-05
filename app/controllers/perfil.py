from app import app
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from app.models.tables import Cliente
from app.__init__ import db


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST': 
        user = Cliente.query.filter_by(email=request.form["username"]).first_or_404()
        print('###############################################################################')
        print(user.email, user.senha, user.id_cliente, user)
        if user.email == request.form['username'] and user.senha == request.form['senha']:
            login_user(user)
            #print(f'Usuário logado: {current_user.username}')
            return redirect(url_for('index'))
        else:
            flash('Login inválido')
        print(user)
    return render_template('/login.html')


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
     logout_user()
    return redirect(url_for('index'))

@app.route('/registrar', methods=['GET', 'POST'])
def registra():
    if request.method == 'POST':
        wUser = request.form['rUsuario']
        wSobrenome = request.form['rSobrenome']
        wCpf_Cnpj = request.form['rcpf_cnpj']
        wCnh = request.form['rcnh']
        wdt_nasc = request.form['rdt_nasc']
        wPw = request.form['rPw']
        wEmail = request.form['rEmail']
        print(request.form)
        usuario = Cliente(nome_cliente=wUser+' '+wSobrenome, cpf_cnpj=wCpf_Cnpj, cnh=wCnh, dt_nasc=wdt_nasc, email=wEmail, senha=wPw)
        #print(usuario)
        db.session.add(usuario)
        db.session.commit()

        #print(usuario)
        #db.session.add(usuario)
        #db.session.commit()
        return redirect('/login')
    return render_template('registro.html')

#DELETAR CONTA
@app.route('/deletar_conta/<id_usuario>')
def deletarConta(id_usuario):
    db.session.delete(Cliente).where(Cliente.id_cliente == id_usuario)
    db.session.commit()