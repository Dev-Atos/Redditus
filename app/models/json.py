from config import baseDir
import json
import os



SAVETO = os.path.join(baseDir,'payload.json')
JSON_FILE = os.path.join(baseDir,'payload.json')

def ler_json():
    with open(JSON_FILE,'r') as f:
        dados = json.load(f)
    return dados

def escrever_json(dados):
    with open(SAVETO, 'w') as arq:
        json.dump(dados,arq,indent=4,default=str)
    
