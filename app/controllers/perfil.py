from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from app.models.comandos_sql import gato
from app.models.tables import Cliente
from app.models.json import escrever_json, ler_json
from app import app
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
                #LOGA O USUÁRIO E O REDIRECIONA PARA última página visitada
                lp = ler_json()
                login_user(user)
                lp['sessao'] = {}
                lp['sessao']['id_usuario'] = str(user.id_cliente)
                lp['sessao']['nome_usuario'] = str(user.nome_cliente)
                lp['sessao']['email'] = str(user.email)
                escrever_json(lp)
                return redirect(lp['sistema']['paginas_visitadas'][0][-1])
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
        dicio = ler_json()
        wUser = request.form['rUsuario']
        wSobrenome = request.form['rSobrenome']
        wCpf_Cnpj = request.form['rcpf_cnpj']
        wCnh = request.form['rcnh']
        wdt_nasc = request.form['rdt_nasc']
        wPw = request.form['rPw']
        wEmail = request.form['rEmail']
        #print(request.form)
        nome_completo = wUser+' '+wSobrenome
        print(request.form)

        #REGISTRA NO BANCO DE DADOS OS DADOS DO CLIENTE E FAZ A CRIPTOGRAFIA(BÁSICÃO) DA SENHA DELE
        query_registra = """INSERT INTO CLIENTE
            SELECT ?,?,?,?,?,?"""
        gato(query_registra, nome_completo, wCpf_Cnpj, wCnh, wdt_nasc, wEmail, generate_password_hash(wPw, method='sha256'),consulta=0)
        db.session.commit()#COMMITA A AÇÃO
        return redirect('login')
    else:
        dicio = ler_json()
        print(dicio)
        return render_template('registro.html',dicio=dicio)#REDIRECIONA O USUÁRIO PARA PÁGINA DE LOGIN


@app.route('/perfil')
def perfil():
    dicio = ler_json()
    info_extra = gato("""
        SELECT CPF_CNPJ,CNH, CONVERT(VARCHAR,DT_NASC,103) FROM CLIENTE
        WHERE ID_CLIENTE = ?""", dicio['sessao']['id_usuario'], consulta=1).fetchall()[0]

    query_executa = """
        SELECT CASE WHEN A.ID_UNIDADE = 1 THEN 'São Miguel'
        WHEN A.ID_UNIDADE = 2 THEN 'São Paulo'
        WHEN A.ID_UNIDADE = 3 THEN 'Guarulhos' 
        WHEN A.ID_UNIDADE = 4 THEN 'Campinas'
        WHEN A.ID_UNIDADE = 5 THEN 'São José dos Campos'
        WHEN A.ID_UNIDADE = 6 THEN 'Santo André' 
        WHEN A.ID_UNIDADE = 7 THEN 'Ribeirão Preto'
        WHEN A.ID_UNIDADE = 8 THEN 'Sorocaba'
        WHEN A.ID_UNIDADE = 9 THEN 'Santos'
        WHEN A.ID_UNIDADE = 10 THEN 'Suzano' 
        WHEN A.ID_UNIDADE = 11 THEN 'Piracicapa'
        WHEN A.ID_UNIDADE = 12 THEN 'Osasco' 
        WHEN A.ID_UNIDADE = 13 THEN 'Barueri'
        WHEN A.ID_UNIDADE = 14 THEN 'Rio de Janeiro'
        WHEN A.ID_UNIDADE = 15 THEN 'Belo Horizonte'
        ELSE 'Carregando...' END AS UNIDADE,
        C.MARCA,C.MODELO,CONVERT(VARCHAR,A.DT_RETIRADA,103),
        CONVERT(VARCHAR,A.DT_DEVOLUCAO,103),CAST(A.VALOR_TOTAL AS NUMERIC(15,2)),A.STATUS_VEIC,A.ID_RESERVA,
        A.ID_VEICULO
        FROM RESERVA A
        INNER JOIN CLIENTE B
        ON A.ID_CLIENTE = B.ID_CLIENTE
        INNER JOIN VEICULO C
        ON A.ID_VEICULO = C.ID_VEICULO
        WHERE A.ID_CLIENTE = ?
        ORDER BY A.ID_RESERVA DESC
        """
    dados = gato(query_executa, dicio['sessao']['id_usuario'],consulta=1).fetchall()

    return render_template('/perfil.html', dicio=dicio, dados_perfil=info_extra,dados_reserva=dados)

#DELETAR CONTA
@app.route('/deletar_conta/<id_usuario>')
def deletarConta(id_usuario):
    logout()
    gato("""DELETE CLIENTE WHERE ID_CLIENTE = ?""", id_usuario,consulta=0)
    return redirect('/')


@app.route('/cancelar_reserva/<id_reserva>/<id_veiculo>')
def cancelar_reserva(id_reserva,id_veiculo):
    query_cancela = """
        UPDATE RESERVA SET STATUS_VEIC = 'CANCELADA'
        WHERE ID_RESERVA = ?

        UPDATE VEICULO SET DISPONIVEL = 1
        WHERE ID_VEICULO = ?
    """
    gato(query_cancela,id_reserva,id_veiculo,consulta=0)
    return redirect(url_for('perfil'))