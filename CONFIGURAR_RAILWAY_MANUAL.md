# 🔧 Configurar Railway Manualmente (Sem Root Directory)

Se a opção "Add Root Directory" não aparecer, configure manualmente:

## ✅ Solução: Configurar Build e Deploy Commands

### 1. Na Seção "Build"

1. Vá em **Settings** → **Build** (no sidebar)
2. Procure por **"Custom Build Command"**
3. Clique em **"+ Build Command"**
4. Digite:
   ```bash
   cd nodejs-app && npm install
   ```
5. Salve

### 2. Na Seção "Deploy"

1. Vá em **Settings** → **Deploy** (no sidebar)
2. Procure por **"Start Command"** ou **"Custom Start Command"**
3. Configure:
   ```bash
   cd nodejs-app && npm start
   ```
4. Salve

### 3. Configurar Variáveis

1. Volte para a página principal do serviço
2. Clique na aba **"Variables"**
3. Adicione:
   - `FOOTBALL_DATA_API_KEY` = `sua_chave_aqui`
   - `PORT` = `3000` (opcional)

### 4. Fazer Deploy

1. O Railway deve fazer deploy automaticamente
2. Ou vá em **"Deployments"** e clique em **"Redeploy"**

---

## ✅ Alternativa: Usar railway.json

O arquivo `railway.json` na raiz já está configurado com os comandos corretos.

1. Faça push para o GitHub:
   ```bash
   git add railway.json
   git commit -m "Update Railway config"
   git push
   ```

2. No Railway, o arquivo será detectado automaticamente
3. Faça um novo deploy

---

## 📝 O que os comandos fazem

- **Build:** `cd nodejs-app && npm install`
  - Entra na pasta `nodejs-app/`
  - Instala as dependências

- **Start:** `cd nodejs-app && npm start`
  - Entra na pasta `nodejs-app/`
  - Inicia o servidor

---

## 🆘 Se ainda não funcionar

Crie um novo serviço:
1. Volte para a página principal do projeto
2. Clique em "+ Create"
3. Selecione "GitHub Repo"
4. Ao conectar, você pode especificar a pasta `nodejs-app` diretamente

