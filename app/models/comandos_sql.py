from config import parametros
import pyodbc

#FUNCAO PARA EXECUTAR COMANDOS SQL
def gato(query_executa, *args, **kwards):
    conexao = pyodbc.connect(parametros)
    cursor = conexao.cursor()
    
    if kwards.get('consulta') == 0:
        cursor.execute(query_executa,[c for c in args])
        cursor.commit()
    elif kwards.get('consulta') == 1:
        return cursor.execute(query_executa,[c for c in args])
    else:
        return f'Especifique a ação: \n\nconsulta=0(UPDATE, DELETE, ETC)\nconsulta=1(select)'