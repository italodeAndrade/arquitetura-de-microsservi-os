import mysql.connector
from mysql.connector import errorcode
import os
from auth import hash_password, verify_password

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


def logar_usuario(email, senha):
    """Autentica usuário verificando email e senha com hash"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        query = "SELECT id, email, senha, nome FROM usuario WHERE email = %s"
        cursor.execute(query, (email,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if usuario and verify_password(senha, usuario[2]):  # usuario[2] é a senha
            return {
                'id': usuario[0],
                'email': usuario[1],
                'nome': usuario[3]
            }
    return None

def criar_usuario(nome, email, senha):
    """Cria novo usuário com senha hasheada"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        senha_hash = hash_password(senha)
        query = "INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s)"
        try:
            cursor.execute(query, (nome, email, senha_hash))
            conn.commit()
            user_id = cursor.lastrowid
            cursor.close()
            conn.close()
            return {
                'id': user_id,
                'nome': nome,
                'email': email
            }
        except mysql.connector.Error as err:
            cursor.close()
            conn.close()
            print(f"Erro ao criar usuário: {err}")
            return None
    return None

def buscar_usuario_por_id(user_id):
    """Busca usuário por ID"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        query = "SELECT id, email, nome FROM usuario WHERE id = %s"
        cursor.execute(query, (user_id,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if usuario:
            return {
                'id': usuario[0],
                'email': usuario[1],
                'nome': usuario[2]
            }
    return None