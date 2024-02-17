from flask import request
from rinha.flask_app import app
from rinha.persistence import dao

@app.route("/clientes/<int:client_number>/transacoes", methods = ['POST'])
def transaction(client_number=None):
    if not request.json:
        return "BAD REQUEST", 422

    client = dao.fetch_client(client_number)
    if not client:
        return "CLIENT NOT FOUND", 404

    transaction = request.json

    try:
        transaction_type = transaction["tipo"]
        transaction_amount = transaction["valor"]
        transaction_description = transaction["descricao"]

        if not transaction_amount or not isinstance(transaction_amount, int) or transaction_amount <= 0 or not transaction_type or transaction_type not in ['c', 'd'] or not transaction_description or len(transaction_description) > 10:
            return "BAD REQUEST", 422

        res = dao.transact(transaction_type, client_number, transaction_amount, transaction_description)
        if not res.success:
            return "NON-SUFFICIENT FUNDS", 422
    except KeyError:
        return "BAD REQUEST", 422

    return {"limite" : client.limit_amount, "saldo" : res.balance}, 200

@app.route("/clientes/<int:client_number>/extrato", methods = ['GET', 'POST'])
def statement(client_number=None):
    res = dao.fetch_statement(client_number)
    if not res:
        return "CLIENT NOT FOUND", 404

    balance = {
        "total": res.balance,
        "data_extrato": res.done.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "limite": res.limit_amount
    }

    trs = []
    for t in res.transactions:
        trs.append({
            "valor": t.amount,
            "tipo": t.transaction_type,
            "descricao": t.description,
            "realizada_em": t.done.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        })

    return {"saldo": balance, "ultimas_transacoes": trs }, 200
