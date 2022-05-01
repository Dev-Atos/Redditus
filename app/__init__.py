from flask import Flask
from flask_login import LoginManager
from flask_script import Manager #Migração banco de dados
from flask_migrate import Migrate, MigrateCommand #migração Banco de dados
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
Bootstrap(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

lm = LoginManager()
lm.init_app(app)

from app.models.tables import Cliente
from app.models.tables import Unidade
from app.models.tables import Administrador
from app.models.tables import Veiculo
from app.models.tables import Reserva
from app.controllers import default,perfil