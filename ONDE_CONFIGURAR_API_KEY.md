# 📍 Onde Configurar a FOOTBALL_DATA_API_KEY

## 🗂️ Locais no Projeto

### 1. **Node.js App** (`nodejs-app/`)

#### Arquivo `.env` (Recomendado)
📁 Localização: `nodejs-app/.env`

```env
FOOTBALL_DATA_API_KEY=sua_chave_aqui
PORT=3000
```

**Como criar:**
```bash
cd nodejs-app
# Windows
echo FOOTBALL_DATA_API_KEY=sua_chave_aqui > .env
echo PORT=3000 >> .env

# Linux/Mac
cat > .env << EOF
FOOTBALL_DATA_API_KEY=sua_chave_aqui
PORT=3000
EOF
```

#### Código que lê a chave:
📄 Arquivo: `nodejs-app/server.js`
- Linha 5: `require('dotenv').config();` - Carrega o `.env`
- A chave é enviada pelo frontend via POST request

#### Interface Web:
📄 Arquivo: `nodejs-app/public/index.html`
- Campo de input na sidebar: `<input type="password" id="apiKey">`

---

### 2. **Streamlit App** (Python)

#### Variável de Ambiente
📁 Localização: Variável de ambiente do sistema

**Windows PowerShell:**
```powershell
$env:FOOTBALL_DATA_API_KEY="sua_chave_aqui"
```

**Windows CMD:**
```cmd
set FOOTBALL_DATA_API_KEY=sua_chave_aqui
```

**Linux/Mac:**
```bash
export FOOTBALL_DATA_API_KEY="sua_chave_aqui"
```

#### Código que lê a chave:
📄 Arquivo: `streamlit_app.py`
- Linha 237: `api_key_env = os.getenv("FOOTBALL_DATA_API_KEY", "").strip()`
- Linha 238: `API_TOKEN = api_key_input.strip() or api_key_env`

#### Interface Web:
📄 Arquivo: `streamlit_app.py`
- Linha 236: Campo de input na sidebar do Streamlit

---

### 3. **Script Python** (`football_top_vs_bottom.py`)

#### Variável de Ambiente
📁 Localização: Variável de ambiente do sistema

```bash
export FOOTBALL_DATA_API_KEY="sua_chave_aqui"
```

#### Código que lê a chave:
📄 Arquivo: `football_top_vs_bottom.py`
- Linha 37: `API_TOKEN = os.getenv("FOOTBALL_DATA_API_KEY", "").strip()`

---

## 🔍 Verificar se Está Configurada

### Node.js:
```bash
cd nodejs-app
# Verificar se .env existe e tem a chave
cat .env | grep FOOTBALL_DATA_API_KEY
```

### Streamlit/Python:
```bash
# Windows PowerShell
$env:FOOTBALL_DATA_API_KEY

# Linux/Mac
echo $FOOTBALL_DATA_API_KEY
```

---

## 📋 Resumo por Projeto

| Projeto | Arquivo de Config | Localização | Como Usar |
|---------|------------------|-------------|-----------|
| **Node.js** | `.env` | `nodejs-app/.env` | Criar arquivo com `FOOTBALL_DATA_API_KEY=...` |
| **Streamlit** | Variável de ambiente | Sistema | `$env:FOOTBALL_DATA_API_KEY="..."` ou campo web |
| **Python Script** | Variável de ambiente | Sistema | `export FOOTBALL_DATA_API_KEY="..."` |

---

## ✅ Checklist de Configuração

### Para Node.js:
- [ ] Criar arquivo `nodejs-app/.env`
- [ ] Adicionar linha: `FOOTBALL_DATA_API_KEY=sua_chave`
- [ ] Verificar se o arquivo está no lugar certo
- [ ] Reiniciar o servidor (`npm start`)

### Para Streamlit:
- [ ] Configurar variável de ambiente OU
- [ ] Digitar a chave no campo do formulário web
- [ ] Verificar se o app lê a chave corretamente

---

## 🆘 Problemas Comuns

### "API token é obrigatório" (Node.js)
- ✅ Verificar se `nodejs-app/.env` existe
- ✅ Verificar se tem a linha `FOOTBALL_DATA_API_KEY=...`
- ✅ Reiniciar o servidor após criar/editar `.env`

### "Defina a API Key" (Streamlit)
- ✅ Configurar variável de ambiente OU
- ✅ Digitar no campo do formulário

### Chave não funciona
- ✅ Verificar se copiou a chave completa
- ✅ Verificar se não há espaços extras
- ✅ Obter nova chave em https://www.football-data.org/

---

## 📚 Mais Informações

Veja o arquivo `COMO_OBTER_API_KEY.md` para:
- Como obter a chave no site football-data.org
- Instruções detalhadas de configuração
- Solução de problemas

