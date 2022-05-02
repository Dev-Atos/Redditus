import pyodbc

#Necessário para conectar
dados_conexao = (
    'Driver={SQL Server};'
    'Server=BRAINIAC\SPDB_BRAINIAC;'
    'Database=DB_BRT;'
)

conexao = pyodbc.connect(dados_conexao)
#Cursor == new Query
cursor = conexao.cursor()

#query_executa = """INSERT INTO ADMINISTRADOR(ID_ADM, NOME, USUARIO, SENHA) VALUES(0,'Admin', 'Redditus', 'adminRed00$')"""
#db = pd.read_sql_query(query_executa, conexao)
#cursor.execute(query_executa)
#ursor.commit()
#display(db)