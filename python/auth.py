import jwt
import bcrypt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
import os

# Configurações JWT
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'sua-chave-secreta-super-segura-aqui')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24

def hash_password(password):
    """Gera hash da senha usando bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password, hashed_password):
    """Verifica se a senha corresponde ao hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_token(user_id, email):
    """Gera token JWT para o usuário"""
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token

def verify_token(token):
    """Verifica e decodifica o token JWT"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator para proteger rotas que requerem autenticação"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Verifica se o token está no header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'message': 'Token malformado'}), 401
        
        if not token:
            return jsonify({'message': 'Token de acesso necessário'}), 401
        
        try:
            payload = verify_token(token)
            if payload is None:
                return jsonify({'message': 'Token inválido ou expirado'}), 401
            
            # Adiciona informações do usuário ao contexto da requisição
            request.current_user = payload
            
        except Exception as e:
            return jsonify({'message': 'Token inválido'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

def get_current_user():
    """Retorna o usuário atual baseado no token JWT"""
    if hasattr(request, 'current_user'):
        return request.current_user
    return None
