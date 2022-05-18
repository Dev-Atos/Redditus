import os.path
from urllib.parse import quote_plus


baseDir = os.path.abspath(os.path.dirname(__file__))

DEBUG=True


parametros = (
    # Driver que será utilizado na conexão
    'DRIVER={SQL Server};'
    # IP ou nome do servidor.
    'SERVER=BRAINIAC\SPDB_BRAINIAC;'
    # Porta
    'PORT=1433;'
    # eu estive aqui
    # Banco que será utilizado.
    'DATABASE=DB_BRT;'
)

url_db = quote_plus(parametros)

SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc:///?odbc_connect=%s' % url_db
SQLALCHEMY_TRACK_MODIFICATIONS = True