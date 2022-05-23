from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app import app
from app.models.calculos import delta_dias, descontin10
from app.models.comandos_sql import gato
from app.models.json import escrever_json, ler_json


@app.route('/pagamento/<id_carro>', methods=['GET','POST'])
@login_required
def pagamento(id_carro):
    dicio = ler_json()
    if request.method == 'POST':
        print(f'PAGAMENTO: s{dicio}')
        escrever_json(dicio)
        reservar(dicio)
        return redirect(url_for('perfil'))
    else:
        dicio['sistema']['id_carro'] = id_carro
        valor_diaria = gato("""SELECT VALOR_DIARIA FROM VEICULO WHERE ID_VEICULO = ?""", id_carro,consulta=1)
        dias = delta_dias(dicio["sistema"]["dt_reserva"])
        dicio['sistema']['valor_diaria'] = f"{abs(float(valor_diaria.fetchone()[0])):.2f}"
        dicio['sistema']['qtd_dias'] = abs(int(dias))
        dicio['sistema']['valor_total_sem_descontin'] = f"{abs(float(float(dicio['sistema']['valor_diaria']) * dias)):.2f}"

        qtd_reservas_cliente = gato("""
                SELECT COUNT(*) FROM RESERVA
                WHERE ID_CLIENTE = ?
        """, dicio['sessao']['id_usuario'],consulta=1)

        #APLICA 10% DE DESCONTO SE FOR PRIMEIRA VEZ QUE O CLIENTE ALUGA
        if int(qtd_reservas_cliente.fetchall()[0][0]) < 1:
            dicio['sistema']['valor_total'] = f"{abs(float(descontin10(dicio['sistema']['valor_diaria'], dias))):.2f}"
        else:
            dicio['sistema']['valor_total'] = f"{abs(float(dicio['sistema']['valor_total_sem_descontin'])):.2f}"

        escrever_json(dicio)

        return render_template('/pagamento.html', dicio=ler_json())

def reservar(dicio):
    gato("""INSERT INTO RESERVA
    SELECT ?,?,?,0,'DEBITO',?,?,?,'RESERVADO'""", 
    int(current_user.get_id),int(dicio['sistema']['id_carro']),
    int(dicio['sistema']['id_unidade']),dicio['sistema']['dt_reserva'][0],
    dicio['sistema']['dt_reserva'][1],float(dicio['sistema']['valor_total']),consulta=0)
    
    gato("""UPDATE VEICULO SET DISPONIVEL = 0
            WHERE ID_VEICULO = ?""", int(dicio['sistema']['id_carro']), consulta=0)
    #print(veic_reserva)