from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():

    return "<h1>Olá! O servidor Flask está funcionando!</h1><p>Você acessou a página principal.</p>"

@app.route('/sobre')
def sobre():

    return "<h1>Página Sobre</h1><p>Este é um exemplo simples de servidor web com Flask.</p>"


if __name__ == '__main__':

    app.run(debug=True)