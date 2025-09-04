from flask import Flask
from flask import Flask, request, jsonify
from db import init_db

app = Flask(__name__)

@app.route('/logar', methods=['POST'])
def logar():
    dados = request.get_json()


    if not dados or not dados.get('email') or not dados.get('senha'):
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    email = dados.get('email')
    senha = dados.get('senha')

    usuario = logar_usuario(email, senha)


    if usuario:

        return jsonify({"message": "Login realizado com sucesso!"})
    else:

        return jsonify({"erro": "Email ou senha inválidos"}), 401


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)