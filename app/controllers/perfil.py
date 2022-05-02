from app import app
from app.models.tables import Cliente
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from app.models.banco_dados import cursor


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST': 
        user = Cliente.query.filter_by(email=request.form["username"]).first()
        #print(user.email, user.password, user.id, user)
        if user.email == request.form['username'] and user.password == request.form['pw']:
            login_user(user)
            #print(f'Usuário logado: {current_user.username}')
            return redirect(url_for('index'))
        else:
            flash('Login inválido')
        print(user)
    return render_template('/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/registrar', methods=['GET', 'POST'])
def registra():
    if request.method == 'POST':
        wUser = request.form['rUsuario']
        wSobrenome = request.form['rUsuario']
        wCpf_Cnpj = request.form['rcpf_cnpj']
        wCnh = request.form['rcnh']
        wdt_nasc = request.form['rdt_nasc']
        wPw = request.form['rPw']
        wEmail = request.form['rEmail']
        print(request.form)
        query_registra = f"""INSERT INTO ADMINISTRADOR(ID_ADM, NOME, USUARIO, SENHA) VALUES(0,?,?,?)"""
        cursor.execute(query_registra, (wUser, wSobrenome, wPw))
        cursor.commit()
        #usuario = Cliente(nome_cliente=wUser, cpf_cnpj=wCpf_Cnpj, cnh=wCnh, dt_nasc=wdt_nasc, email=wEmail, senha=wPw)
        #print(usuario)
        #db.session.add(usuario)
        #db.session.commit()
        return redirect('/login')
    return render_template('registro.html')

#DELETAR CONTA