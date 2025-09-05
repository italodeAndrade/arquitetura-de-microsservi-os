from flask import Flask, request, jsonify
from db import logar_usuario, criar_usuario, buscar_usuario_por_id
from auth import generate_token, token_required, get_current_user

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    """Endpoint para login de usuário"""
    dados = request.get_json()

    if not dados or not dados.get('email') or not dados.get('senha'):
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    email = dados.get('email')
    senha = dados.get('senha')

    usuario = logar_usuario(email, senha)

    if usuario:
        # Gera token JWT
        token = generate_token(usuario['id'], usuario['email'])
        
        return jsonify({
            "message": "Login realizado com sucesso!",
            "token": token,
            "user": {
                "id": usuario['id'],
                "nome": usuario['nome'],
                "email": usuario['email']
            }
        })
    else:
        return jsonify({"erro": "Email ou senha inválidos"}), 401

@app.route('/register', methods=['POST'])
def register():
    """Endpoint para registro de novo usuário"""
    dados = request.get_json()

    if not dados or not dados.get('nome') or not dados.get('email') or not dados.get('senha'):
        return jsonify({"erro": "Nome, email e senha são obrigatórios"}), 400

    nome = dados.get('nome')
    email = dados.get('email')
    senha = dados.get('senha')

    # Verifica se usuário já existe
    usuario_existente = logar_usuario(email, senha)
    if usuario_existente:
        return jsonify({"erro": "Usuário já existe"}), 409

    novo_usuario = criar_usuario(nome, email, senha)

    if novo_usuario:
        # Gera token JWT para o novo usuário
        token = generate_token(novo_usuario['id'], novo_usuario['email'])
        
        return jsonify({
            "message": "Usuário criado com sucesso!",
            "token": token,
            "user": {
                "id": novo_usuario['id'],
                "nome": novo_usuario['nome'],
                "email": novo_usuario['email']
            }
        }), 201
    else:
        return jsonify({"erro": "Erro ao criar usuário"}), 500

@app.route('/profile', methods=['GET'])
@token_required
def profile():
    """Endpoint protegido para obter perfil do usuário"""
    current_user = get_current_user()
    
    if not current_user:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    
    user_id = current_user['user_id']
    usuario = buscar_usuario_por_id(user_id)
    
    if usuario:
        return jsonify({
            "user": {
                "id": usuario['id'],
                "nome": usuario['nome'],
                "email": usuario['email']
            }
        })
    else:
        # Se não encontrar no banco, retornar dados do token (para usuários de teste)
        return jsonify({
            "user": {
                "id": current_user['user_id'],
                "nome": "Usuario Teste",
                "email": current_user['email']
            }
        })

@app.route('/protected', methods=['GET'])
@token_required
def protected_route():
    """Exemplo de rota protegida"""
    current_user = get_current_user()
    
    return jsonify({
        "message": "Esta é uma rota protegida!",
        "user": {
            "id": current_user['user_id'],
            "email": current_user['email']
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check (não protegido)"""
    return jsonify({"status": "OK", "message": "API funcionando"})

@app.route('/test-login', methods=['POST'])
def test_login():
    """Endpoint de teste que funciona sem banco"""
    dados = request.get_json()
    
    if not dados or not dados.get('email') or not dados.get('senha'):
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400
    
    email = dados.get('email')
    senha = dados.get('senha')
    
    # Simular usuário válido para teste
    if email == "teste@teste.com" and senha == "123":
        # Simular dados do usuário
        usuario = {
            'id': 1,
            'email': email,
            'nome': 'Usuario Teste'
        }
        
        # Gerar token JWT
        token = generate_token(usuario['id'], usuario['email'])
        
        return jsonify({
            "message": "Login realizado com sucesso!",
            "token": token,
            "user": usuario
        })
    else:
        return jsonify({"erro": "Email ou senha inválidos"}), 401

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)