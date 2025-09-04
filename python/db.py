import mysql.connector
from mysql.connector import errorcode
import os

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASS', 'Simba8!#'),
            database=os.getenv('DB_NAME', 'rouppa')
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None


def logar_usuario(email,senha):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        query = "SELECT * FROM usuario WHERE email = %s AND senha = %s"
        cursor.execute(query, (email, senha))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        return usuario
    return None