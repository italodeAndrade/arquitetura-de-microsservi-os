Este é um trabalho com fins educacionais, o assunto do trabalho é o uso de microsserviços. Escolhemos usar um serviço de Node.js para servir como API Gateway.
Portanto, para a preparação do ambiente para que o trabalho rode de forma correta:

1-AMBIENTE NODE- 
abra um terminal dentro da pasta raiz do node e use os comandos 
```bash
  npm i
```
2-AMBIENTE FLASK- 
abra um terminal dentro da pasta raiz do flask na pasta python e use os comandos:
```bash
  python -m venv .venv
  .\.venv\Scripts\activate
  pip install -r requirements.txt
```

3-AMBIENTE DOCKER-
abra um terminal dentro da pasta raiz node e digite:
```bash
  docker build -t node-gateway .
  docker run -d --rm -p 3000:3000 --name node-container node-gateway
```
  
abra um terminal dentro da pasta raiz do flaske digite:
```bash
  docker build -t servico-python .
  docker run -d -p 5001:5000 --name python-container servico-python
```
  
