from http import HTTPStatus
import pyodbc
from app import app, lm
from app.models.tables import Cliente, Reserva, Veiculo
from flask import abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from datetime import date
from app.__init__ import db
from config import parametros


#NECESSÁRIO PARA NÃO DAR ERRO, VERIFICA SE HÁ USUÁRIO SE NÃO TIVER NENHUM ELE CONTINUA MESMO SEM USUÁRIO
@lm.user_loader
def load_user(id_cliente):
    try:
        user = Cliente.query.get(int(id_cliente))
        #print(f'AQUIIIIIIIIIIIIIIIIIIIIIIIII: {user.nome_cliente}')
        return user
    except Exception as e:
        print (e)
        return None

#SE O USUÁRIO(ANÔNIMO) TENTAR ENTRAR EM ALGUMA PARTE QUE SEJA NECESSÁRIO ESTAR LOGADO ELE CAI PARA LOGIN
@lm.unauthorized_handler
def unauthorized():
    if request.blueprint == 'api':
        abort(HTTPStatus.UNAUTHORIZED)
    return redirect(url_for('login'))

@app.route('/')
def index():
    data_atual = date.today() #Para desabilitar datas anteriores a atual
    usuario = load_user(current_user.get_id)
    dicio = {'user':usuario, 'data_atual':data_atual}
    return render_template('/index.html', dicio=dicio)

#DESENVOLVENDO...
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/busca/<id_unidade>', methods=['GET','POST'])
#@login_required #NECESSÁRIO O USUÁRIO ESTAR LOGADO, CASO NÃO ESTEJA ELE SERÁ REDIRECIONADO PELA FUNÇÃO unauthorized
def busca(id_unidade):
    dicio = request.form
    if request.method == 'POST':
        if id_unidade == '0':
            id_unidade = dicio['id_unidade']
            print(f'IDDDD UNIDADE: {id_unidade}')
            carros_unidade = Veiculo.query.filter_by(id_unidade=int(id_unidade),disponivel=1).all()
            return render_template('busca.html',carros_unidade=carros_unidade, user=load_user(current_user.get_id), dicio=dicio) #, user=usuario
        else:
            if request.form['id_unidade']:
                id_unidade = dicio['id_unidade']
                print('CAIU AQUIIIIII')
    else:
        carros_unidade = Veiculo.query.filter_by(id_unidade=int(id_unidade),disponivel=1).all()
        return render_template('busca.html',carros_unidade=carros_unidade, user=load_user(current_user.get_id), dicio=dicio)


@app.route('/pagamento/<id_unidade>/<id_carro>')
@login_required
def pagamento(id_unidade,id_carro):
    print(f'ID da UNIDADE: {id_unidade}\nID DO CARRO: {id_carro}')
    usuario = load_user(current_user.get_id)
    return render_template('/pagamento.html', user=usuario, id_unidade=id_unidade, id_carro=id_carro)


@app.route('/reservar/<id_unidade>/<id_carro>',methods=['GET', 'POST'])
def reservar(id_unidade,id_carro):
    if request.method == 'POST':
        print(current_user.get_id, type(current_user.get_id))
        reserva = Reserva(id_cliente=int(current_user.get_id),id_veiculo=id_carro, id_unidade=id_unidade,id_adm=0,tp_pagamento='Débito',dt_retirada='2022-05-11', dt_devolucao='2022-05-12',valor_total=250, status_veic='RESERVADO')
        gato(id_carro)
        #print(veic_reserva)
        db.session.add(reserva)#ADICIONA NO BD
        db.session.commit()#COMMITA A AÇÃO
        return 'POST'
    return 'GET'

def gato(id_carro):
    #Necessário para conectar
    conexao = pyodbc.connect(parametros)
    #Cursor == new Query
    cursor = conexao.cursor()
    query_executa = ("""UPDATE VEICULO SET DISPONIVEL = 0 WHERE ID_VEICULO = ?""")
    cursor.execute(query_executa,id_carro)
    cursor.commit()




        #REGISTRA NO BANCO DE DADOS OS DADOS DO CLIENTE E FAZ A CRIPTOGRAFIA(BÁSICÃO) DA SENHA DELE
        #usuario = Cliente(nome_cliente=wUser+' '+wSobrenome, cpf_cnpj=wCpf_Cnpj, cnh=wCnh, dt_nasc=wdt_nasc, email=wEmail, senha=generate_password_hash(wPw, method='sha256'))
        #db.session.add(usuario)#ADICIONA NO BD
        #db.session.commit()#COMMITA A AÇÃO

#CRUD
"""
@app.route('/add',methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        estudantes = Estudantes(nome=request.form['nome'], idade=request.form['idade']) #precisa passar os campos senão dá erro
        db.session.add(estudantes)
        db.session.commit() #Precisa commitar
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<id>', methods=['GET','POST'])
def edit(id):
    estudantes = Estudantes.query.get(id)
    if request.method == 'POST':
        estudantes.nome = request.form['nome']
        estudantes.idade = request.form['idade']
        db.session.commit()
        return redirect(url_for('index'))    
    return render_template('edit.html', estudantes=estudantes)
        

@app.route('/delete/<id>')
def delete(id):
    estudante = Estudantes.query.get(id)
    db.session.delete(estudante)
    db.session.commit()
    return redirect(url_for('index'))
"""