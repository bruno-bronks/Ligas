# 🌐 Como Publicar o App na Internet

## 🚀 Opção Mais Rápida: Railway

### Passo a Passo:

1. **Acesse Railway:**
   - https://railway.app/
   - Faça login com GitHub

2. **Crie Novo Projeto:**
   - Clique em "New Project"
   - Selecione "Deploy from GitHub repo"
   - Escolha seu repositório
   - Selecione a pasta `nodejs-app`

3. **Configure Variáveis:**
   - Vá em "Variables"
   - Adicione: `FOOTBALL_DATA_API_KEY` = `sua_chave_aqui`

4. **Aguarde Deploy:**
   - Railway faz deploy automático
   - Aguarde 2-5 minutos

5. **Copie a URL:**
   - Railway gera uma URL automaticamente
   - Exemplo: `https://seu-app.up.railway.app`

6. **Atualize App Android:**
   - Edite `android-app/app/src/main/java/com/ligas/football/MainActivity.java`
   - Altere: `private static final String APP_URL = "https://sua-url.railway.app";`

### ✅ Pronto!

Seu app está acessível na internet! 🎉

---

## 📚 Mais Opções

Veja `nodejs-app/COMO_PUBLICAR_NA_INTERNET.md` para:
- Render (alternativa gratuita)
- Heroku
- VPS próprio
- Configuração de domínio customizado
- HTTPS/SSL

---

## 🔗 Links Rápidos

- **Railway:** https://railway.app/
- **Render:** https://render.com/
- **Documentação completa:** `nodejs-app/COMO_PUBLICAR_NA_INTERNET.md`

