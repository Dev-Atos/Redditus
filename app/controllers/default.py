from http import HTTPStatus
import pyodbc
from app.models.json import escrever_json, ler_json
from tomlkit import string
from app import app, lm
from app.models.tables import Cliente, Reserva, Veiculo
from flask import abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from datetime import date
from app.__init__ import db
from config import parametros
from pandas import read_sql

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
    usuario = load_user(current_user.get_id)
    if usuario:
        dicio = {
            'sessao':{
                'id_usuario': usuario.id_cliente,
                'nome_usuario': usuario.nome_cliente
            },
            'data_minima': string(date.today())
        }
        escrever_json(dicio)
        return render_template('/index.html', dicio=dicio)
    else:
        dicio = {'data_minima': string(date.today()), 'pagina_visitadas':['/']}
        escrever_json(dicio)
        print(ler_json())
        return render_template('/index.html',dicio=ler_json())

#DESENVOLVENDO...
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/busca/<id_unidade>', methods=['GET','POST'])
#@login_required #NECESSÁRIO O USUÁRIO ESTAR LOGADO, CASO NÃO ESTEJA ELE SERÁ REDIRECIONADO PELA FUNÇÃO unauthorized
def busca(id_unidade):
    if request.method == 'POST':
        dicio = ler_json()
        print(dicio)
        dicio['id_unidade'] = request.form['id_unidade']
        dicio['pagina_visitadas'].append(f'/busca/{request.form["id_unidade"]}')
        print(f'Aquiiiiiiiiiiiiiiiiii: {dicio} tipo {type(dicio)}')
        if id_unidade == '0':
            print('POSTTTTTTTTTTTT')
            carros_unidade = Veiculo.query.filter_by(id_unidade=int(dicio['id_unidade']),disponivel=1).all()
            escrever_json(dicio)
            return render_template('busca.html',carros_unidade=carros_unidade, user=load_user(current_user.get_id), dicio=ler_json()) #, user=usuario
        else:
            id_unidade = '0'
    else:
        print('GETTTTTTTT')
        dicio = ler_json()
        dicio['pagina_visitadas'].append(f'/busca/{dicio["id_unidade"]}')
        print(dicio)
        carros_unidade = Veiculo.query.filter_by(id_unidade=int(dicio['id_unidade']),disponivel=1).all()
        return render_template('busca.html',carros_unidade=carros_unidade, user=load_user(current_user.get_id), dicio=ler_json())


@app.route('/pagamento/<id_unidade>/<id_carro>', methods=['GET','POST'])
@login_required
def pagamento(id_unidade,id_carro):
    dicio = ler_json()
    if request.method == 'POST':
        dicio['id_carro'] = id_carro
        print(dicio)
        escrever_json(dicio)
        return render_template('/pagamento.html', dicio=ler_json())
    else:
        return render_template('/pagamento.html', dicio=ler_json())

def reservar(id_unidade,id_carro):
    if request.method == 'POST':
        print(current_user.get_id, type(current_user.get_id))
        gato("""INSERT INTO RESERVA
        SELECT ?,?,?,0,'DEBITO',?,?,?,'RESERVADO'""", 
        int(current_user.get_id),id_carro,id_unidade,'dt_retirada','dt_devolucao','valor_total',consulta=1)
        #Reserva(id_cliente=int(current_user.get_id),id_veiculo=id_carro, id_unidade=id_unidade,id_adm=0,tp_pagamento='Débito',dt_retirada='2022-05-11', dt_devolucao='2022-05-12',valor_total=250, status_veic='RESERVADO')
        gato("""UPDATE VEICULO SET DISPONIVEL = 0
                WHERE ID_VEICULO = ?""", id_carro, consulta=0)
        #print(veic_reserva)
        db.session.commit()#COMMITA A AÇÃO
        return 'POST'
    return 'GET'

#FUNCAO PARA EXECUTAR COMANDOS SQL
def gato(query_executa, *args, **kwards):
    conexao = pyodbc.connect(parametros)
    cursor = conexao.cursor()
    if kwards.get('consulta') == 0:
        cursor.execute(query_executa,[c for c in args])
        cursor.commit()
        return 'UPDATE FEITO COM SUCESSO !'
    elif kwards.get('consulta') == 1:
        return read_sql(query_executa,conexao)
    else:
        return f'Especifique a ação: \n\nconsulta=0(UPDATE, DELETE, ETC)\nconsulta=1(select)'


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