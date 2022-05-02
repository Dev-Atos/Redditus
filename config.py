import os.path


baseDir = os.path.abspath(os.path.dirname(__file__))


DEBUG=True
SECRET_KEY = 'SUCODELARANJA'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(baseDir,'storage.db') #Configuração do Banco de dados que será utilizado
SQLALCHEMY_TRACK_MODIFICATIONS = True