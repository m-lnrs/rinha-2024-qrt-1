from loguru import logger
from rinha.flask_app import pool
from rinha.model import Client, Balance, Response, Statement, Transaction

def fetch_client(client_number):
    with pool.connection() as connection:
        rs = connection.execute("SELECT * FROM client WHERE number = %s", (client_number,)).fetchone()
        return Client(**dict(zip(("number","name","limit_amount"), rs)))

def fetch_client_balance(client_number):
    with pool.connection() as connection:
        rs = connection.execute("SELECT * FROM balance JOIN client ON client.number = balance.client_number WHERE balance.client_number = %s", (client_number,)).fetchone()
        balance = Balance(**dict(zip(("number","client_number","amount"), rs[0:3])))
        balance.client = Client(**dict(zip(("number","name","limit_amount"), rs[3:])))
        return balance

def credit(client_number, amount, description):
    with pool.connection() as conn:
        rs = conn.execute("SELECT * FROM credit(%s, %s, %s)", (client_number, amount, description)).fetchone()
        return Response(**dict(zip(("balance","success","message"), rs)))

def debit(client_number, amount, description):
    with pool.connection() as conn:
        rs = conn.execute("SELECT * FROM debit(%s, %s, %s)", (client_number, amount, description)).fetchone()
        return Response(**dict(zip(("balance","success","message"), rs)))

def transact(transaction_type, client_number, amount, description):
    if transaction_type == 'c':
        with pool.connection() as conn:
            rs = conn.execute("SELECT * FROM credit(%s, %s, %s)", (client_number, amount, description)).fetchone()
            return Response(**dict(zip(("balance","success","message"), rs)))
    if transaction_type == 'd':
        with pool.connection() as conn:
            rs = conn.execute("SELECT * FROM debit(%s, %s, %s)", (client_number, amount, description)).fetchone()
            return Response(**dict(zip(("balance","success","message"), rs)))
    return None

def fetch_statement(client_number):
    with pool.connection() as conn:
        rs = conn.execute("SELECT balance.amount, NOW(), client.limit_amount FROM client JOIN balance ON balance.client_number = client.number WHERE client.number = %s", (client_number,)).fetchone()
        statement = Statement(**dict(zip(("balance","done","limit_amount"), rs))) if rs else None

        if statement:
            statement.transactions = []
            cursor = conn.execute("SELECT * FROM transaction WHERE transaction.client_number = %s ORDER BY done DESC LIMIT 10", (client_number,))
            for t in cursor:
                statement.transactions.append(Transaction(**dict(zip(("number","client_number","amount","transaction_type","description","done"), t))))
            return statement

    return None
