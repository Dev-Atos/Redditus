from app import db, lm

class Administrador(db.Model):

    id_adm = db.Column('id_adm', db.Integer, primary_key=True)
    nome = db.Column('nome',db.String(255))
    usuario = db.Column('usuario',db.String(255))
    senha = db.Column('senha',db.String(255))

    def __self__(self, usuario, senha): #Para ser possível a instanciação de classe
        self.usuario = usuario
        self.senha = senha

class Unidade(db.Model):

    id_unidade = db.Column('id_unidade',db.Integer, primary_key=True)
    cep = db.Column('cep',db.String(8))
    numero_endereco = db.Column('numero_endereco',db.String(5))

    def __self__(self, cep, numero_endereco): #Para ser possível a instanciação de classe
        self.cep = cep
        self.numero_endereco = numero_endereco

class Veiculo(db.Model):

    id_veiculo = db.Column('id_veiculo',db.Integer, primary_key=True)
    id_unidade = db.Column('id_unidade',db.Integer, db.ForeignKey(Unidade.id_unidade))
    placa = db.Column('placa',db.String(7))
    marca = db.Column('marca',db.String(255))
    modelo = db.Column('modelo',db.String(255))
    cam_aut = db.Column('cam_aut',db.BOOLEAN)
    cor = db.Column('cor',db.String(255))
    cap_pessoas = db.Column('cap_pessoas',db.String(2))
    qtd_portas = db.Column('qtd_portas',db.String(2))
    ano = db.Column('ano',db.String)
    valor_diaria = db.Column('valor_diaria',db.String(2))
    disponivel = db.Column('disponivel',db.Integer)
   
    def __self__(self,  id_veiculo, disponivel): #Para ser possível a instanciação de classe
            self.id_veiculo = id_veiculo
            self.disponivel = disponivel

class Cliente(db.Model):

    id_cliente = db.Column('id_cliente', db.Integer, primary_key=True, autoincrement=True)
    nome_cliente = db.Column('nome_cliente',db.String(255))
    cpf_cnpj = db.Column('cpf_cnpj',db.String(14))
    cnh = db.Column('cnh',db.String(11))
    dt_nasc = db.Column('dt_nasc',db.DATE)
    email = db.Column(db.String(255))
    senha = db.Column(db.String(255))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def get_id(self):
        return str(self.id_cliente)
    
    @lm.user_loader
    def load_user(self):
     return Cliente.get(self.id_cliente)


    def __self__(self,  nome_cliente, email, senha): #Para ser possível a instanciação de classe
        self.username = nome_cliente
        self.email = email
        self.senha = senha

class Reserva(db.Model):
    id_cliente = db.Column('id_cliente',db.Integer, db.ForeignKey(Cliente.id_cliente))
    id_reserva = db.Column('id_reserva',db.Integer, primary_key=True)
    id_veiculo = db.Column('id_veiculo',db.Integer, db.ForeignKey(Veiculo.id_veiculo))
    id_unidade = db.Column('id_unidade',db.Integer, db.ForeignKey(Unidade.id_unidade))
    id_adm = db.Column('id_adm',db.Integer, db.ForeignKey(Administrador.id_adm))
    tp_pagamento = db.Column('tp_pagamento',db.String(255))
    dt_retirada = db.Column('dt_retirada',db.DATE)
    dt_devolucao = db.Column('dt_devolucao',db.DATE)
    valor_total = db.Column('valor_total',db.String(255))
    status_veic = db.Column('status_veic',db.String(255))