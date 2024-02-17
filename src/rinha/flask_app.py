import os

from flask import Flask
from loguru import logger
from psycopg_pool import ConnectionPool, AsyncConnectionPool

user = os.environ.get("DATABASE_USER", default="admin")
password = os.environ.get("DATABASE_PASS", default="123")
host = os.environ.get("DATABASE_HOST", default="127.0.0.1")
port = os.environ.get("DATABASE_PORT", default="5432")
database = os.environ.get("DATABASE_NAME", default="rinha")

min_size = os.environ.get("DATABASE_MIN_POOL_SIZE", default=1)
max_size = os.environ.get("DATABASE_MAX_POOL_SIZE", default=10)

app = Flask(__name__)

logger.debug("creating connection pool")
connection = f"host={host} port={port} dbname={database} user={user} password={password}"
pool = ConnectionPool(connection, min_size=int(min_size), max_size=int(max_size), open=True)
