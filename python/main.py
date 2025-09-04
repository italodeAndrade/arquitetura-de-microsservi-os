from flask import Flask

app = Flask(__name__)

@app.route('/logar', methods=['POST'])
def logar():
    query = 'select * from usuarios where email = :email and senha = :senha'
    
