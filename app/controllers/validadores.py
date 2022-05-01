#NÃO ESTÁ SENDO USADO POR ENQUANTO

def valida_cpf(cpf):
    cpf = cpf.replace('.', '').replace('-', '').strip()
    cpf_verifica = cpf
    cpf = cpf[0:9]
    while len(cpf) != 11:
        digito = sum([int(cpf[index]) * multiplica for index,
                     multiplica in enumerate(reversed(range(2, len(cpf)+2)))])
        cpf += str(11 - (digito % 11)) if (11 - (digito % 11)) <= 9 else '0'
    return True if cpf == cpf_verifica and cpf != (str(cpf[0]) * len(cpf)) else False


def valida_cnpj(cnpj):
    cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '').strip()
    cnpj_verifica = cnpj
    cnpj = cnpj[0:12]
    while len(cnpj) != 14:
        digito = 0
        multiplica = 5 if len(cnpj) < 13 else 6
        for n in cnpj:
            digito += (int(n) * multiplica)
            multiplica -= 1
            multiplica = 9 if multiplica == 1 else multiplica
        dv = 11 - (digito % 11)
        cnpj += '0' if dv > 9 else str(dv)
    return True if cnpj == cnpj_verifica and cnpj != (str(cnpj[0]) * len(cnpj)) else False