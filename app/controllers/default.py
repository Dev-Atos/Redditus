from app import app, lm
from app.models.tables import Users
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user,current_user
from app. __init__ import db


#NECESSÁRIO PARA NÃO DAR ERRO, VERIFICA O USUÁRIO SE NÃO TIVER NENHUM ELE CONTINUA MESMO SEM USUÁRIO
@lm.user_loader
def load_user(id):
    try:
        user = Users.query.get(int(id))
        #print(f'AQUIIIIIIIIIIIIIIIIIIIIIIIII: {user.username}')
        return user
    except Exception as e:
        print (e)
        return None


@app.route('/')
def index():
    return render_template('/index.html')#, user=current_user

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST': 
        user = Users.query.filter_by(email=request.form["username"]).first()
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
        rUser = request.form['rUsername']
        rPw = request.form['rPw']
        rEmail = request.form['rEmail']
        #query_registra = (f"INSERT INTO USERS VALUES(username={rUser}, email={rEmail}, password={rPw})")
        usuario = Users(username=rUser, email=rEmail, password=rPw)
        print(usuario)
        db.session.add(usuario)
        db.session.commit()
        return redirect('/login')
    return render_template('registro.html')