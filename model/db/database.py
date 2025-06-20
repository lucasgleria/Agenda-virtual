import psycopg2.pool
from .config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

# Pool de conexões para otimizar a comunicação com o banco
db_pool = psycopg2.pool.SimpleConnectionPool(
    1, 10,
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

def get_db_connection():
    """Obtém uma conexão do pool."""
    return db_pool.getconn()

def release_db_connection(conn):
    """Devolve a conexão ao pool."""
    db_pool.putconn(conn) 