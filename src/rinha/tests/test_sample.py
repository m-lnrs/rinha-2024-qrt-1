# curl --header "Content-Type: application/json" --request POST --data '{"valor": 1000, "tipo": "c", "descricao": "descricao"}' http://127.0.0.1:5000/clientes/1/transacoes

from rinha.controller.MainController import app

def test_negative_transaction_value():
    app.testing = True
    response = app.test_client().post("/clientes/1/transacoes", json={"valor": -1000, "tipo": "c", "descricao": "descricao"})
    assert response.status_code == 422
    
def test_float_transaction_value():
    app.testing = True
    response = app.test_client().post("/clientes/1/transacoes", json={"valor": 1000.0, "tipo": "c", "descricao": "descricao"})
    assert response.status_code == 422

def test_string_transaction_value():
    app.testing = True
    response = app.test_client().post("/clientes/1/transacoes", json={"valor": "1000", "tipo": "c", "descricao": "descricao"})
    assert response.status_code == 422

def test_wrong_transaction_type():
    app.testing = True
    response = app.test_client().post("/clientes/1/transacoes", json={"valor": 1000, "tipo": "b", "descricao": "descricao"})
    assert response.status_code == 422
    
def test_missing_json_transaction_value():
    app.testing = True
    response = app.test_client().post("/clientes/1/transacoes", json={"tipo": "c", "descricao": "descricao"})
    assert response.status_code == 422

def test_missing_json_transaction_type():
    app.testing = True
    response = app.test_client().post("/clientes/1/transacoes", json={"valor": 1000, "descricao": "descricao"})
    assert response.status_code == 422

def test_missing_json_transaction_description():
    app.testing = True
    response = app.test_client().post("/clientes/1/transacoes", json={"valor": 1000, "tipo": "c"})
    assert response.status_code == 422

def test_not_numeric_url_parameter():
    app.testing = True
    response = app.test_client().post("/clientes/1a/transacoes", json={"valor": 1000, "tipo": "c", "descricao": "descricao"})
    assert response.status_code == 404


