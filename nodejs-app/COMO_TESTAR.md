# 🧪 Como Testar o App Node.js

Este guia mostra como testar o servidor Node.js em diferentes cenários.

## 📋 Índice

1. [Testar Servidor Localmente](#1-testar-servidor-localmente)
2. [Testar API Endpoints](#2-testar-api-endpoints)
3. [Testar no Navegador](#3-testar-no-navegador)
4. [Testar no App Android](#4-testar-no-app-android)
5. [Testar em Produção](#5-testar-em-produção)
6. [Solução de Problemas](#solução-de-problemas)

---

## 1. Testar Servidor Localmente

### Passo 1: Verificar Pré-requisitos

```bash
# Verificar se Node.js está instalado
node --version
# Deve mostrar: v16.x.x ou superior

# Verificar se npm está instalado
npm --version
```

### Passo 2: Instalar Dependências

```bash
cd nodejs-app
npm install
```

Você deve ver:
```
added X packages, and audited Y packages
```

### Passo 3: Configurar API Key

Crie o arquivo `.env`:

```bash
# Windows PowerShell
cd nodejs-app
@"
FOOTBALL_DATA_API_KEY=sua_chave_aqui
PORT=3000
"@ | Out-File -FilePath .env -Encoding utf8

# Linux/Mac
cd nodejs-app
cat > .env << EOF
FOOTBALL_DATA_API_KEY=sua_chave_aqui
PORT=3000
EOF
```

### Passo 4: Iniciar o Servidor

```bash
npm start
```

Você deve ver:
```
🚀 Servidor rodando em http://localhost:3000
📱 Configure o app Android para: http://localhost:3000
```

### ✅ Verificar se Está Funcionando

Abra outro terminal e teste:

```bash
# Health check
curl http://localhost:3000/health

# Deve retornar:
# {"status":"ok","timestamp":"2024-..."}
```

---

## 2. Testar API Endpoints

### Teste 1: Health Check

```bash
# Via curl
curl http://localhost:3000/health

# Via PowerShell
Invoke-WebRequest -Uri http://localhost:3000/health

# Resposta esperada:
# {"status":"ok","timestamp":"2024-01-01T12:00:00.000Z"}
```

### Teste 2: Buscar Dados de uma Liga

```bash
# Via curl (Linux/Mac)
curl -X POST http://localhost:3000/api/league-data \
  -H "Content-Type: application/json" \
  -d '{
    "token": "sua_chave_aqui",
    "leagueCode": "PL",
    "daysAhead": 10
  }'

# Via PowerShell (Windows)
$body = @{
    token = "sua_chave_aqui"
    leagueCode = "PL"
    daysAhead = 10
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:3000/api/league-data `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

**Resposta esperada:**
```json
{
  "standings": [...],
  "strengths": [...],
  "fixtures": [...],
  "probabilities": [...]
}
```

### Teste 3: Limpar Cache

```bash
# Via curl
curl -X POST http://localhost:3000/api/clear-cache

# Resposta esperada:
# {"message":"Cache limpo"}
```

### Teste 4: Verificar Erro sem Token

```bash
curl -X POST http://localhost:3000/api/league-data \
  -H "Content-Type: application/json" \
  -d '{"leagueCode": "PL"}'

# Resposta esperada:
# {"error":"API token é obrigatório"}
```

---

## 3. Testar no Navegador

### Passo 1: Abrir o App

1. Certifique-se de que o servidor está rodando
2. Abra o navegador
3. Acesse: `http://localhost:3000`

### Passo 2: Verificar Interface

Você deve ver:
- ✅ Sidebar com controles à esquerda
- ✅ Campo para API Key
- ✅ Seleção de ligas
- ✅ Slider de dias
- ✅ Botões de atualizar

### Passo 3: Testar Funcionalidades

1. **Digite a API Key** no campo
2. **Selecione uma liga** (ex: Premier League)
3. **Clique em "🔄 Atualizar"**
4. **Aguarde o carregamento**

### ✅ Verificar Resultados

Você deve ver:
- ✅ Tabela de classificação
- ✅ Próximos jogos
- ✅ Probabilidades calculadas
- ✅ Alertas Top-3 vs Bottom-3
- ✅ Botões de download CSV

### Teste de Download CSV

1. Clique em "⬇️ Baixar CSV (Classificação)"
2. Verifique se o arquivo é baixado
3. Abra o CSV e verifique os dados

---

## 4. Testar no App Android

### Cenário A: Emulador Android

#### Passo 1: Iniciar o Servidor Node.js

```bash
cd nodejs-app
npm start
```

#### Passo 2: Configurar URL no App Android

Edite `android-app/app/src/main/java/com/ligas/football/MainActivity.java`:

```java
private static final String APP_URL = "http://10.0.2.2:3000";
```

**Importante:** `10.0.2.2` é o endereço especial do emulador que aponta para `localhost` do computador.

#### Passo 3: Executar o App

1. Abra o Android Studio
2. Inicie um emulador
3. Execute o app (▶️ Run)
4. O app deve carregar o dashboard

### Cenário B: Dispositivo Físico

#### Passo 1: Descobrir IP do Computador

**Windows:**
```powershell
ipconfig
# Procure por "Endereço IPv4" (ex: 192.168.1.100)
```

**Linux/Mac:**
```bash
ifconfig
# ou
ip addr show
```

#### Passo 2: Iniciar Servidor com IP Público

O servidor já aceita conexões externas por padrão. Certifique-se de que:
- Firewall permite conexões na porta 3000
- Computador e dispositivo estão na mesma rede Wi-Fi

#### Passo 3: Configurar URL no App Android

```java
private static final String APP_URL = "http://192.168.1.100:3000";
```
(Substitua pelo IP do seu computador)

#### Passo 4: Testar no Dispositivo

1. Conecte o dispositivo via USB
2. Execute o app
3. Verifique se carrega corretamente

### ✅ Checklist de Testes Android

- [ ] App abre sem erros
- [ ] WebView carrega a interface
- [ ] Barra de progresso funciona
- [ ] É possível digitar a API Key
- [ ] Dados são carregados corretamente
- [ ] Tabelas são exibidas
- [ ] Download CSV funciona
- [ ] Botão voltar funciona

---

## 5. Testar em Produção

### Teste 1: Verificar Servidor Online

```bash
# Substitua pela URL do seu servidor
curl https://seu-servidor.com/health
```

### Teste 2: Testar API em Produção

```bash
curl -X POST https://seu-servidor.com/api/league-data \
  -H "Content-Type: application/json" \
  -d '{
    "token": "sua_chave",
    "leagueCode": "PL",
    "daysAhead": 10
  }'
```

### Teste 3: Verificar HTTPS

- ✅ Certifique-se de que está usando HTTPS
- ✅ Verifique se o certificado SSL é válido
- ✅ Teste no navegador e no app Android

---

## 🔍 Verificar Logs

### Logs do Servidor

O servidor mostra logs no console:

```bash
# Inicie o servidor
npm start

# Você verá:
# 🚀 Servidor rodando em http://localhost:3000
# 📱 Configure o app Android para: http://localhost:3000

# Quando houver requisições:
# (logs de requisições aparecerão aqui)
```

### Logs de Erro

Se houver erros, eles aparecerão no console:

```
Erro ao buscar dados: Error: ...
```

### Modo Desenvolvimento (Mais Logs)

```bash
npm run dev
```

Isso usa `nodemon` que mostra mais informações.

---

## 🐛 Solução de Problemas

### Problema: Servidor não inicia

**Sintomas:**
```
Error: Cannot find module 'express'
```

**Solução:**
```bash
cd nodejs-app
npm install
```

### Problema: Porta 3000 já em uso

**Sintomas:**
```
Error: listen EADDRINUSE: address already in use :::3000
```

**Solução:**
1. Altere a porta no `.env`:
   ```env
   PORT=3001
   ```
2. Ou mate o processo na porta 3000:
   ```bash
   # Windows
   netstat -ano | findstr :3000
   taskkill /PID <PID> /F
   
   # Linux/Mac
   lsof -ti:3000 | xargs kill
   ```

### Problema: API Key não funciona

**Sintomas:**
```
{"error":"API token é obrigatório"}
```

**Solução:**
1. Verifique se o `.env` existe em `nodejs-app/`
2. Verifique se a chave está correta
3. Ou digite a chave no campo do formulário web

### Problema: Erro 429 (Rate Limit)

**Sintomas:**
```
HTTP 429: Too Many Requests
```

**Solução:**
- O app tem retry automático
- Aguarde alguns minutos
- Cache de 60s reduz chamadas
- Considere fazer upgrade da conta no football-data.org

### Problema: App Android não carrega

**Sintomas:**
- Tela em branco
- Erro de conexão

**Solução:**
1. Verifique se o servidor está rodando
2. Verifique a URL no `MainActivity.java`
3. Para emulador, use `10.0.2.2:3000`
4. Para dispositivo físico, use o IP do computador
5. Teste a URL no navegador do dispositivo primeiro

### Problema: CORS Error

**Sintomas:**
```
Access to fetch at '...' from origin '...' has been blocked by CORS policy
```

**Solução:**
O servidor já tem CORS habilitado. Se ainda houver problemas, verifique `server.js` linha 12:
```javascript
app.use(cors());
```

---

## 📊 Testes de Performance

### Teste de Cache

1. Faça uma requisição (deve demorar alguns segundos)
2. Faça a mesma requisição novamente (deve ser instantânea - cache)

### Teste de Múltiplas Ligas

1. Selecione várias ligas
2. Clique em "Atualizar"
3. Verifique se todas carregam corretamente

### Teste de Retry

1. Desconecte a internet temporariamente
2. Faça uma requisição
3. Reconecte
4. O app deve tentar novamente automaticamente

---

## ✅ Checklist Completo de Testes

### Servidor
- [ ] Servidor inicia sem erros
- [ ] Health check retorna OK
- [ ] API endpoints funcionam
- [ ] Cache funciona
- [ ] Retry funciona

### Interface Web
- [ ] Página carrega corretamente
- [ ] Formulário funciona
- [ ] Dados são exibidos
- [ ] Download CSV funciona
- [ ] Responsivo (mobile/desktop)

### App Android
- [ ] App abre
- [ ] WebView carrega
- [ ] Dados são exibidos
- [ ] Interações funcionam
- [ ] Botão voltar funciona

### Produção
- [ ] HTTPS funciona
- [ ] Servidor estável
- [ ] Performance adequada
- [ ] Logs funcionam

---

## 🧪 Testes Automatizados (Opcional)

### Criar Teste Simples

Crie `nodejs-app/test.js`:

```javascript
const axios = require('axios');

async function test() {
  try {
    // Health check
    const health = await axios.get('http://localhost:3000/health');
    console.log('✅ Health check:', health.data);
    
    // API test
    const data = await axios.post('http://localhost:3000/api/league-data', {
      token: process.env.FOOTBALL_DATA_API_KEY,
      leagueCode: 'PL',
      daysAhead: 10
    });
    console.log('✅ API test:', data.data.standings.length, 'teams');
  } catch (error) {
    console.error('❌ Test failed:', error.message);
  }
}

test();
```

Execute:
```bash
node test.js
```

---

## 📝 Notas Finais

- Sempre teste localmente antes de fazer deploy
- Verifique os logs para identificar problemas
- Teste em diferentes navegadores
- Teste no app Android em diferentes dispositivos
- Para produção, use HTTPS e configure adequadamente

---

## 🆘 Precisa de Ajuda?

- Verifique os logs do servidor
- Teste os endpoints individualmente
- Verifique a documentação da API: https://www.football-data.org/documentation
- Consulte `README.md` para mais informações

