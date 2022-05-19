from http import HTTPStatus
from app.models.calculos import delta_dias, descontin10
from app.models.comandos_sql import gato
from app.models.json import escrever_json, ler_json
from tomlkit import string
from app import app, lm
from app.models.tables import Cliente, Veiculo
from flask import abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from datetime import date
from app.__init__ import db


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
                'nome_usuario': usuario.nome_cliente,
                'email': usuario.email
            },
            'sistema':{
                'data_minima': string(date.today())
            }
        }
        escrever_json(dicio)
        return render_template('/index.html', dicio=dicio)
    else:
        dicio = {'sistema':{
                'data_minima': string(date.today())
            }}
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
        dicio['sistema']['id_unidade'] = request.form['id_unidade']
        dicio['sistema']['dt_reserva'] = [request.form['dt_retirada'],request.form['dt_devolucao']]
        print(f'Aquiiiiiiiiiiiiiiiiii: {dicio} tipo {type(dicio)}')
        if id_unidade == '0':
            print('POSTTTTTTTTTTTT')
            carros_unidade = Veiculo.query.filter_by(id_unidade=int(dicio['sistema']['id_unidade']),disponivel=1).all()
            escrever_json(dicio)
            return render_template('busca.html',carros_unidade=carros_unidade, user=load_user(current_user.get_id), dicio=ler_json()) #, user=usuario
        else:
            id_unidade = '0'
    else:
        print('GETTTTTTTT')
        dicio = ler_json()
        print(dicio)
        carros_unidade = Veiculo.query.filter_by(id_unidade=int(dicio['sistema']['id_unidade']),disponivel=1).all()
        return render_template('busca.html',carros_unidade=carros_unidade, user=load_user(current_user.get_id), dicio=ler_json())


@app.route('/pagamento/<id_carro>', methods=['GET','POST'])
@login_required
def pagamento(id_carro):
    dicio = ler_json()
    if request.method == 'POST':
        dicio['sistema']['id_carro'] = id_carro
        print(f'PAGAMENTO: s{dicio}')
        escrever_json(dicio)
        return render_template('/pagamento.html', dicio=ler_json())
    else:
        valor_diaria = gato("""SELECT VALOR_DIARIA FROM VEICULO WHERE ID_VEICULO = ?""", id_carro,consulta=1)
        dias = delta_dias(dicio["sistema"]["dt_reserva"])
        dicio['sistema']['valor_diaria'] = f"{float(valor_diaria.fetchone()[0]):,.2f}"
        dicio['sistema']['qtd_dias'] = dias
        dicio['sistema']['valor_total_sem_descontin'] = f"R$ {float(float(dicio['sistema']['valor_diaria']) * dias):.2f}"
        dicio['sistema']['valor_total'] = f"R$ {descontin10(dicio['sistema']['valor_diaria'], dias):.2f}"
        escrever_json(dicio)
        return render_template('/pagamento.html', dicio=ler_json())

def reservar(id_unidade,id_carro):
    gato("""INSERT INTO RESERVA
    SELECT ?,?,?,0,'DEBITO',?,?,?,'RESERVADO'""", 
    int(current_user.get_id),id_carro,id_unidade,'dt_retirada','dt_devolucao','valor_total',consulta=1)
    #Reserva(id_cliente=int(current_user.get_id),id_veiculo=id_carro, id_unidade=id_unidade,id_adm=0,tp_pagamento='Débito',dt_retirada='2022-05-11', dt_devolucao='2022-05-12',valor_total=250, status_veic='RESERVADO')
    gato("""UPDATE VEICULO SET DISPONIVEL = 0
            WHERE ID_VEICULO = ?""", id_carro, consulta=0)
    #print(veic_reserva)
    db.session.commit()#COMMITA A AÇÃO