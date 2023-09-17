import psycopg2
from psycopg2.extras import RealDictCursor
class Connection:
    db_params = {
        "host": "localhost",
        "database": "postgres",
        "user": "postgres",
        "password": "admin"
    }

    def conn(self):
        try:
            conn = psycopg2.connect(**Connection.db_params)
        except:
         print("Connessione non riuscita")
        return conn

    def close(conn):
        conn.close()