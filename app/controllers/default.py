from fileinput import filename
from http import HTTPStatus
from app import app, lm
from app.models.tables import Cliente, Veiculo
from flask import abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required


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
    return render_template('/index.html', user=usuario)

#DESENVOLVENDO...
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/busca', methods=['GET','POST'])
@login_required #NECESSÁRIO O USUÁRIO ESTAR LOGADO, CASO NÃO ESTEJA ELE SERÁ REDIRECIONADO PELA FUNÇÃO unauthorized
def busca():
    if request.method == 'POST':
        id_unidade = request.form['id_unidade']
        #usuario = load_user(current_user.get_id)
        carros_unidade = Veiculo.query.filter_by(id_unidade=int(id_unidade),disponivel=1).all()
    return render_template('/busca.html',carros_unidade=carros_unidade) #, user=usuario

@app.route('/pagamento')
@login_required
def pagamento():
    usuario = load_user(current_user.get_id)
    return render_template('/pagamento.html', user=usuario)


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