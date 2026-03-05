from myLib import p1Settings
import psycopg

def connect():
    print(f"Intentando conectar a {p1Settings.POSTGRES_DB} en {p1Settings.POSTGRES_HOST}...")
    conn= psycopg.connect(
        dbname=p1Settings.POSTGRES_DB,
        user=p1Settings.POSTGRES_USER,
        password=p1Settings.POSTGRES_PASSWORD,
        host=p1Settings.POSTGRES_HOST,
        port=p1Settings.POSTGRES_PORT
        )
    print("Connected")
    return conn