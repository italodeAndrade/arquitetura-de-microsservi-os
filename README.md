Este é um trabalho com fins educacionais, o assunto do trabalho é o uso de microsserviços. Escolhemos usar um serviço de Node.js para servir como API Gateway.

## 🚀 Configuração do Ambiente

### ⚡ OPÇÃO 1: Docker Compose (RECOMENDADO - Sem Erros)

Execute na pasta raiz do projeto:
```bash
docker-compose up --build
```

### 🔧 OPÇÃO 2: Configuração Manual

#### 1. AMBIENTE NODE
Abra um terminal na pasta `node` e execute:
```bash
npm install
```

#### 2. AMBIENTE PYTHON (Se Python estiver instalado)
Abra um terminal na pasta `python` e execute:
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

#### 3. AMBIENTE DOCKER (Manual - CORRIGIDO)

**⚠️ IMPORTANTE: Execute os comandos Docker na PASTA RAIZ do projeto**

**Para o serviço Node:**
```bash
# Na pasta raiz do projeto (não na pasta node!)
docker build -t node-gateway ./node
docker run -d --rm -p 3000:3000 --name node-container node-gateway
```

**Para o serviço Python:**
```bash
# Na pasta raiz do projeto (não na pasta python!)
docker build -t servico-python ./python
docker run -d -p 5001:5000 --name python-container servico-python
```

## 🔧 Solução de Problemas

### ❌ "docker-compose: O termo não é reconhecido"
**Problema:** Docker não está instalado
**Solução:** 
1. Baixe Docker Desktop: https://www.docker.com/products/docker-desktop/
2. Instale e reinicie o computador
3. Abra Docker Desktop e aguarde inicializar
4. Teste: `docker --version`

### ❌ "Python não foi encontrado"
**Solução:** Instale o Python em https://www.python.org/downloads/
- ⚠️ **IMPORTANTE:** Marque "Add Python to PATH" durante a instalação

### ❌ "npm: command not found"
**Solução:** Instale o Node.js em https://nodejs.org/

### ❌ Erro nos comandos Docker
**Problema:** Comandos executados na pasta errada
**Solução:** Use a **OPÇÃO 1 (Docker Compose)** ou execute os comandos Docker na pasta raiz do projeto

## 🚀 Alternativa: Executar sem Docker

Se não quiser instalar Docker, você pode executar os serviços diretamente:

### Node.js (API Gateway)
```bash
# Na pasta node
npm install
npm run dev
```

### Python (Flask API)
```bash
# Na pasta python (após instalar Python)
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
  
