# ⚡ Testar Rápido - Node.js App

## 🚀 Teste em 3 Passos

### 1. Iniciar o Servidor

```bash
cd nodejs-app
npm start
```

### 2. Abrir no Navegador

Abra: http://localhost:3000

### 3. Testar

1. Digite sua API Key no campo
2. Selecione uma liga
3. Clique em "🔄 Atualizar"
4. Verifique se os dados aparecem

## ✅ Se Funcionou

- ✅ Servidor está OK
- ✅ API está funcionando
- ✅ Interface está correta

## ❌ Se Não Funcionou

### Erro: "Cannot find module"
```bash
npm install
```

### Erro: "Porta já em uso"
```bash
# Altere PORT no .env para 3001
```

### Erro: "API token é obrigatório"
- Crie arquivo `.env` com `FOOTBALL_DATA_API_KEY=...`
- Ou digite a chave no formulário web

## 🧪 Teste Rápido da API

```bash
# Health check
curl http://localhost:3000/health

# Deve retornar: {"status":"ok",...}
```

## 📱 Testar no Android

1. Configure URL: `http://10.0.2.2:3000` (emulador)
2. Execute o app
3. Verifique se carrega

## 📚 Mais Detalhes

Veja `COMO_TESTAR.md` para guia completo.

