# 🔑 Como Obter e Configurar a FOOTBALL_DATA_API_KEY

## 📍 O que é?

A `FOOTBALL_DATA_API_KEY` é uma chave de API necessária para acessar os dados do site **football-data.org**, que fornece informações sobre ligas de futebol, classificações e jogos.

## 🔐 Como Obter a Chave

### Passo 1: Criar Conta

1. Acesse: https://www.football-data.org/
2. Clique em **"Sign Up"** ou **"Register"**
3. Preencha o formulário de registro
4. Confirme seu email

### Passo 2: Obter a API Key

1. Faça login na sua conta
2. Vá em **"Account"** ou **"API"**
3. Você verá sua **API Token** ou **API Key**
4. Copie essa chave (ela será algo como: `abc123def456ghi789...`)

### Tipos de Conta

- **Free Tier**: Gratuito, mas com limite de requisições
- **Paid Tier**: Mais requisições e acesso a mais dados

Para começar, a conta gratuita é suficiente!

## ⚙️ Como Configurar no Projeto

### Opção 1: Arquivo `.env` (Recomendado)

#### Para Node.js:

1. Na pasta `nodejs-app/`, crie um arquivo chamado `.env`
2. Adicione:

```env
FOOTBALL_DATA_API_KEY=sua_chave_aqui
PORT=3000
```

**Exemplo:**
```env
FOOTBALL_DATA_API_KEY=abc123def456ghi789jkl012mno345pqr678
PORT=3000
```

#### Para Streamlit (Python):

1. Na raiz do projeto, crie um arquivo `.env`
2. Adicione:

```env
FOOTBALL_DATA_API_KEY=sua_chave_aqui
```

**Nota:** Para Streamlit, você também pode usar variável de ambiente diretamente.

### Opção 2: Variável de Ambiente do Sistema

#### Windows (PowerShell):

```powershell
# Temporário (apenas nesta sessão)
$env:FOOTBALL_DATA_API_KEY="sua_chave_aqui"

# Permanente (para o usuário)
[System.Environment]::SetEnvironmentVariable('FOOTBALL_DATA_API_KEY', 'sua_chave_aqui', 'User')
```

#### Windows (CMD):

```cmd
set FOOTBALL_DATA_API_KEY=sua_chave_aqui
```

#### Linux/Mac:

```bash
# Temporário
export FOOTBALL_DATA_API_KEY="sua_chave_aqui"

# Permanente (adicione ao ~/.bashrc ou ~/.zshrc)
echo 'export FOOTBALL_DATA_API_KEY="sua_chave_aqui"' >> ~/.bashrc
source ~/.bashrc
```

### Opção 3: Interface Web (Streamlit)

No app Streamlit, você pode digitar a chave diretamente no campo do formulário lateral. A chave será usada apenas durante a sessão.

### Opção 4: Interface Web (Node.js)

No app Node.js, você pode digitar a chave no campo "API Key" do formulário. A chave será enviada em cada requisição.

## 📂 Onde a Chave é Usada no Código

### Node.js (`nodejs-app/server.js`)

A chave é lida do arquivo `.env` através do `dotenv`:

```javascript
require('dotenv').config();
// A chave pode ser acessada via process.env.FOOTBALL_DATA_API_KEY
```

Mas no código atual, a chave é enviada pelo frontend via POST request.

### Streamlit (`streamlit_app.py`)

```python
# Linha 237-238
api_key_env = os.getenv("FOOTBALL_DATA_API_KEY", "").strip()
API_TOKEN = api_key_input.strip() or api_key_env
```

A chave é lida de:
1. Campo de input na interface (prioridade)
2. Variável de ambiente `FOOTBALL_DATA_API_KEY`

## 🔍 Verificar se Está Configurada

### Node.js:

```bash
# Verificar se o .env existe
cd nodejs-app
cat .env  # Linux/Mac
type .env  # Windows CMD
Get-Content .env  # Windows PowerShell
```

### Streamlit:

```bash
# Verificar variável de ambiente
echo $FOOTBALL_DATA_API_KEY  # Linux/Mac
echo %FOOTBALL_DATA_API_KEY%  # Windows CMD
$env:FOOTBALL_DATA_API_KEY  # Windows PowerShell
```

## 🧪 Testar se a Chave Funciona

### Via cURL (Terminal):

```bash
curl -H "X-Auth-Token: sua_chave_aqui" https://api.football-data.org/v4/competitions/PL/standings
```

Se retornar dados JSON, a chave está funcionando! ✅

### Via Navegador:

1. Abra o app (Node.js ou Streamlit)
2. Digite a chave no campo
3. Selecione uma liga
4. Clique em "Atualizar"
5. Se os dados aparecerem, está funcionando! ✅

## ⚠️ Problemas Comuns

### Erro: "API token é obrigatório"

**Solução:**
- Verifique se o arquivo `.env` existe
- Verifique se a chave está escrita corretamente (sem espaços extras)
- Reinicie o servidor após criar/editar o `.env`

### Erro: "HTTP 401: Unauthorized"

**Solução:**
- A chave está incorreta ou expirada
- Obtenha uma nova chave no site football-data.org
- Verifique se copiou a chave completa (sem cortes)

### Erro: "HTTP 429: Too Many Requests"

**Solução:**
- Você atingiu o limite de requisições da sua conta
- Aguarde alguns minutos
- Considere fazer upgrade para conta paga

### A chave não é lida

**Solução:**
- Certifique-se de que o arquivo `.env` está na pasta correta:
  - Node.js: `nodejs-app/.env`
  - Streamlit: raiz do projeto `.env`
- Verifique se não há espaços antes/depois do `=`
- Reinicie o servidor

## 🔒 Segurança

### ⚠️ IMPORTANTE: Não Compartilhe sua Chave!

- ❌ **NÃO** commite o arquivo `.env` no Git
- ❌ **NÃO** compartilhe a chave publicamente
- ✅ O arquivo `.env` já está no `.gitignore`
- ✅ Use variáveis de ambiente em produção

### Verificar se `.env` está no `.gitignore`:

```bash
# Verificar .gitignore
cat .gitignore  # Linux/Mac
type .gitignore  # Windows
```

O arquivo `.env` deve estar listado no `.gitignore`!

## 📝 Resumo Rápido

1. **Obter chave**: https://www.football-data.org/ → Sign Up → Account → API Token
2. **Configurar**: Criar arquivo `.env` com `FOOTBALL_DATA_API_KEY=sua_chave`
3. **Testar**: Iniciar o app e verificar se os dados carregam
4. **Problemas?**: Verificar se a chave está correta e se o `.env` está no lugar certo

## 🆘 Precisa de Ajuda?

- Documentação da API: https://www.football-data.org/documentation/quickstart
- Suporte: Verifique a seção de FAQ no site
- Limites: Consulte a página de planos no site

