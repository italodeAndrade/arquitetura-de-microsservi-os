# 🚀 COMANDOS PARA TESTAR JWT

## 1. Iniciar o Servidor
```bash
cd python
python main.py
```

## 2. Comandos de Teste (PowerShell)

### Health Check
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/health" -Method GET
```

### Registrar Usuário
```powershell
$body = @{nome="Joao"; email="joao@teste.com"; senha="123"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/register" -Method POST -Body $body -ContentType "application/json"
```

### Fazer Login
```powershell
$body = @{email="joao@teste.com"; senha="123"} | ConvertTo-Json
$response = Invoke-RestMethod -Uri "http://localhost:5000/login" -Method POST -Body $body -ContentType "application/json"
$token = $response.token
Write-Host "Token: $token"
```

### Testar Rota Protegida
```powershell
$headers = @{"Authorization" = "Bearer $token"}
Invoke-RestMethod -Uri "http://localhost:5000/protected" -Method GET -Headers $headers
```

### Ver Perfil
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/profile" -Method GET -Headers $headers
```

### Testar Token Inválido (deve dar erro 401)
```powershell
$invalidHeaders = @{"Authorization" = "Bearer token_invalido"}
Invoke-RestMethod -Uri "http://localhost:5000/protected" -Method GET -Headers $invalidHeaders
```

## 🎯 Sequência Completa (Copie e Cole)

```powershell
# 1. Health Check
Invoke-RestMethod -Uri "http://localhost:5000/health" -Method GET

# 2. Teste de Login (funciona sem banco)
$loginBody = @{email="teste@teste.com"; senha="123"} | ConvertTo-Json
$loginResponse = Invoke-RestMethod -Uri "http://localhost:5000/test-login" -Method POST -Body $loginBody -ContentType "application/json"
$token = $loginResponse.token
Write-Host "Login: $($loginResponse.message)"
Write-Host "Token: $token"

# 3. Usar token para rota protegida
$headers = @{"Authorization" = "Bearer $token"}
$protectedResponse = Invoke-RestMethod -Uri "http://localhost:5000/protected" -Method GET -Headers $headers
Write-Host "Protegida: $($protectedResponse.message)"

# 4. Ver perfil
$profileResponse = Invoke-RestMethod -Uri "http://localhost:5000/profile" -Method GET -Headers $headers
Write-Host "Perfil: $($profileResponse.user.nome)"

# 5. Testar token inválido (deve dar erro)
$invalidHeaders = @{"Authorization" = "Bearer token_invalido"}
try {
    Invoke-RestMethod -Uri "http://localhost:5000/protected" -Method GET -Headers $invalidHeaders
} catch {
    Write-Host "✅ Token inválido detectado corretamente: $($_.Exception.Message)"
}
```

## ✅ Respostas Esperadas:

- **Health Check**: `{"status": "OK", "message": "API funcionando"}`
- **Test Login**: `{"message": "Login realizado com sucesso!", "token": "...", "user": {...}}`
- **Rota Protegida**: `{"message": "Esta é uma rota protegida!", "user": {...}}`
- **Perfil**: `{"user": {"id": 1, "nome": "Usuario Teste", "email": "teste@teste.com"}}`
- **Token Inválido**: Erro 401 com mensagem de token inválido

## 🗄️ USAR COM BANCO DE DADOS MYSQL

### 1. Iniciar MySQL
```bash
# Via XAMPP/WAMP ou
net start mysql
```

### 2. Criar Tabela
```sql
USE rouppa;

CREATE TABLE IF NOT EXISTS usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Comandos com Banco Real

#### Registrar Usuário Real
```powershell
$body = @{nome="Joao Silva"; email="joao@teste.com"; senha="senha123"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/register" -Method POST -Body $body -ContentType "application/json"
```

#### Login Real
```powershell
$body = @{email="joao@teste.com"; senha="senha123"} | ConvertTo-Json
$response = Invoke-RestMethod -Uri "http://localhost:5000/login" -Method POST -Body $body -ContentType "application/json"
$token = $response.token
Write-Host "Token: $token"
```

#### Usar Token
```powershell
$headers = @{"Authorization" = "Bearer $token"}
Invoke-RestMethod -Uri "http://localhost:5000/protected" -Method GET -Headers $headers
Invoke-RestMethod -Uri "http://localhost:5000/profile" -Method GET -Headers $headers
```

### 4. Configuração do Banco (db.py)
- **Host**: localhost
- **Usuário**: root  
- **Senha**: Simba8!#
- **Banco**: rouppa

Para alterar, edite as linhas 9-12 do arquivo `db.py`

## 🐛 Problemas Comuns:

- **Erro 500**: MySQL não está rodando
- **Erro 401**: Token inválido ou expirado
- **Erro de conexão**: Servidor não está rodando
- **Erro ao criar usuário**: Tabela não existe ou credenciais erradas
