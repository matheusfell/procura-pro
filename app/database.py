import psycopg2
from psycopg2 import pool

# Criar o pool de conexões
try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(1, 20, "postgresql://diego:135790@localhost:5432/procurapro")
    print("Conexão com o PostgreSQL criada com sucesso")
except (Exception, psycopg2.DatabaseError) as error:
    print("Erro ao conectar ao PostgreSQL", error)

# Função para obter uma conexão do pool
def get_db():
    conn = connection_pool.getconn()
    try:
        yield conn
    finally:
        connection_pool.putconn(conn)

# Funções para executar operações de banco de dados

def execute_query(query, params=None):
    """
    Executa uma consulta INSERT, UPDATE, DELETE.
    """
    conn = connection_pool.getconn()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        print("Query executada com sucesso")
    except Exception as e:
        conn.rollback()
        print(f"Erro ao executar a query: {e}")
    finally:
        connection_pool.putconn(conn)

def fetch_query(query, params=None):
    """
    Executa uma consulta SELECT.
    """
    conn = connection_pool.getconn()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        return results
    except Exception as e:
        print(f"Erro ao executar a query: {e}")
        return []
    finally:
        connection_pool.putconn(conn)