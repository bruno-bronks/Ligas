# ⚡ Deploy Rápido - 5 Minutos

## 🚂 Railway (Mais Rápido)

### 1. Criar Conta
- Acesse: https://railway.app/
- Login com GitHub

### 2. Novo Projeto
- "New Project" → "Deploy from GitHub repo"
- Selecione seu repositório
- Escolha pasta `nodejs-app`

### 3. Variáveis
- Settings → Variables
- Adicione: `FOOTBALL_DATA_API_KEY=sua_chave`

### 4. Pronto!
- Railway gera URL automaticamente
- Exemplo: `https://seu-app.up.railway.app`

---

## 🎨 Render (Alternativa)

### 1. Criar Conta
- Acesse: https://render.com/
- Login com GitHub

### 2. Novo Web Service
- "New +" → "Web Service"
- Conecte repositório
- Pasta: `nodejs-app`

### 3. Configurar
- Build: `npm install`
- Start: `npm start`
- Plan: Free

### 4. Variáveis
- Environment Variables
- `FOOTBALL_DATA_API_KEY=sua_chave`

### 5. Deploy
- "Create Web Service"
- Aguarde 5-10 minutos
- URL: `https://seu-app.onrender.com`

---

## 📱 Atualizar Android

Edite `android-app/app/src/main/java/com/ligas/football/MainActivity.java`:

```java
private static final String APP_URL = "https://seu-app.railway.app";
```

---

## ✅ Testar

1. Abra a URL no navegador
2. Teste o app
3. Teste no app Android

**Pronto! Seu app está na internet! 🎉**

