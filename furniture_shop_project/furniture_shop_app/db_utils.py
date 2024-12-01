import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        dbname='furniture_shop',
        user='postgres',
        password='pass',
        host='localhost',
        port='5432'
    )
    return conn