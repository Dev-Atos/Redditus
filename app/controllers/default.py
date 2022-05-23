from http import HTTPStatus
from app.models.calculos import delta_dias, descontin10
from app.models.comandos_sql import gato
from app.models.json import escrever_json, ler_json
from tomlkit import string
from app import app, lm
from app.models.tables import Cliente, Veiculo
from flask import abort, redirect, render_template, request, url_for
from flask_login import current_user, fresh_login_required, login_required
from datetime import date

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
                'data_minima': string(date.today()),
                'paginas_visitadas':[['/']]
            }
        }
        escrever_json(dicio)
        return render_template('/index.html', dicio=dicio)
    else:
        dicio = {'sistema':{
                'data_minima': string(date.today()),
                'paginas_visitadas':[['/']]
            }}
        escrever_json(dicio)
        print(ler_json())
        return render_template('/index.html',dicio=ler_json())

#DESENVOLVENDO...
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/busca/<id_unidade>', methods=['GET','POST'])
@login_required #NECESSÁRIO O USUÁRIO ESTAR LOGADO, CASO NÃO ESTEJA ELE SERÁ REDIRECIONADO PELA FUNÇÃO unauthorized
def busca(id_unidade):
    if request.method == 'POST':
        dicio = ler_json()
        dicio['sistema']['id_unidade'] = request.form['id_unidade']
        dicio['sistema']['dt_reserva'] = [request.form['dt_retirada'],request.form['dt_devolucao']]
        dicio['sistema']['paginas_visitadas'][0].append(f'/busca/{dicio["sistema"]["id_unidade"]}')
    
        if id_unidade == '0':
            carros_unidade = Veiculo.query.filter_by(id_unidade=int(dicio['sistema']['id_unidade']),disponivel=1).all()
            print(request.referrer)
            escrever_json(dicio)
            return render_template('busca.html',carros_unidade=carros_unidade, user=load_user(current_user.get_id), dicio=ler_json())
        else:
            id_unidade = '0'
    else:
        dicio = ler_json()
        carros_unidade = Veiculo.query.filter_by(id_unidade=int(dicio['sistema']['id_unidade']),disponivel=1).all()
        return render_template('busca.html',carros_unidade=carros_unidade, user=load_user(current_user.get_id), dicio=ler_json())