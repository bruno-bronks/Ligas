# 🔑 Configurar API Key - Guia Rápido

## 📍 Onde Criar o Arquivo `.env`

Crie o arquivo `.env` **nesta pasta**: `nodejs-app/`

```
Ligas/
└── nodejs-app/
    ├── .env          ← CRIE AQUI!
    ├── server.js
    ├── package.json
    └── ...
```

## ✏️ Conteúdo do Arquivo `.env`

Crie o arquivo `nodejs-app/.env` com este conteúdo:

```env
FOOTBALL_DATA_API_KEY=sua_chave_aqui
PORT=3000
```

**Exemplo real:**
```env
FOOTBALL_DATA_API_KEY=abc123def456ghi789jkl012mno345pqr678
PORT=3000
```

## 🖥️ Como Criar (Windows)

### Opção 1: Notepad
1. Abra o Notepad
2. Digite:
   ```
   FOOTBALL_DATA_API_KEY=sua_chave_aqui
   PORT=3000
   ```
3. Salve como: `nodejs-app\.env` (sem extensão .txt!)

### Opção 2: PowerShell
```powershell
cd nodejs-app
@"
FOOTBALL_DATA_API_KEY=sua_chave_aqui
PORT=3000
"@ | Out-File -FilePath .env -Encoding utf8
```

### Opção 3: CMD
```cmd
cd nodejs-app
echo FOOTBALL_DATA_API_KEY=sua_chave_aqui > .env
echo PORT=3000 >> .env
```

## 🐧 Como Criar (Linux/Mac)

```bash
cd nodejs-app
cat > .env << EOF
FOOTBALL_DATA_API_KEY=sua_chave_aqui
PORT=3000
EOF
```

## ✅ Verificar se Funcionou

```bash
cd nodejs-app
# Windows
type .env

# Linux/Mac
cat .env
```

Você deve ver:
```
FOOTBALL_DATA_API_KEY=sua_chave_aqui
PORT=3000
```

## 🚀 Depois de Criar

1. Reinicie o servidor Node.js:
   ```bash
   npm start
   ```

2. A chave será carregada automaticamente!

## ⚠️ Importante

- ❌ **NÃO** commite o arquivo `.env` no Git (já está no `.gitignore`)
- ✅ Substitua `sua_chave_aqui` pela sua chave real
- ✅ Não adicione espaços antes/depois do `=`
- ✅ Não use aspas na chave (a menos que a chave tenha espaços)

## 🔐 Onde Obter a Chave?

1. Acesse: https://www.football-data.org/
2. Crie uma conta (gratuita)
3. Vá em "Account" → "API Token"
4. Copie a chave

## 🆘 Problemas?

- **Arquivo não encontrado**: Certifique-se de que está na pasta `nodejs-app/`
- **Chave não funciona**: Verifique se copiou a chave completa
- **Erro ao iniciar**: Verifique se não há espaços extras no arquivo

