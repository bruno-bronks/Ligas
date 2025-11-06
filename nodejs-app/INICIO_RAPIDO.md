# 🚀 Início Rápido - Node.js App

## Passo 1: Instalar Node.js

Baixe em: https://nodejs.org/ (versão 16 ou superior)

## Passo 2: Instalar Dependências

```bash
cd nodejs-app
npm install
```

## Passo 3: Configurar API Key

Crie um arquivo `.env` na pasta `nodejs-app/`:

```env
FOOTBALL_DATA_API_KEY=sua_chave_aqui
PORT=3000
```

**OU** use variável de ambiente:

```bash
# Windows PowerShell
$env:FOOTBALL_DATA_API_KEY="sua_chave"

# Linux/Mac
export FOOTBALL_DATA_API_KEY="sua_chave"
```

## Passo 4: Iniciar o Servidor

```bash
npm start
```

Você verá:
```
🚀 Servidor rodando em http://localhost:3000
📱 Configure o app Android para: http://localhost:3000
```

## Passo 5: Testar no Navegador

Abra: http://localhost:3000

## Passo 6: Testar no App Android

1. Certifique-se de que o servidor está rodando
2. Configure a URL no `MainActivity.java`:
   - Emulador: `http://10.0.2.2:3000`
   - Dispositivo físico: `http://IP_DO_COMPUTADOR:3000`
3. Execute o app Android

## ✅ Pronto!

O app Node.js está funcionando e substitui completamente o Streamlit.

## 🔧 Comandos Úteis

```bash
# Modo desenvolvimento (auto-reload)
npm run dev

# Verificar se está rodando
curl http://localhost:3000/health
```

## 📝 Notas

- Porta padrão: **3000** (diferente do Streamlit que usa 8501)
- API Key pode ser configurada no `.env` ou no formulário web
- Cache automático de 60 segundos
- Retry automático em caso de rate limit

