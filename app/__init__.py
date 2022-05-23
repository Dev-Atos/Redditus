from flask import Flask
from flask_login import LoginManager
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.from_object('config')

app.secret_key='SUCODELARANJA'

db = SQLAlchemy(app)

manager = Manager(app)

lm = LoginManager()
lm.init_app(app)

from app.models.tables import Cliente
from app.models.tables import Veiculo
from app.controllers import default,perfil,reservar