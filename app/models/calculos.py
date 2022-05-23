from datetime import datetime

def descontin10(valor_diaria, delta_dias):
    return float(valor_diaria) * int(delta_dias) * 0.90

def delta_dias(dias):
    data1 = datetime.strptime(dias[0], '%Y-%m-%d')
    data2 = datetime.strptime(dias[1], '%Y-%m-%d')
    return (data2-data1).days