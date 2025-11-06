# 🌐 Como Publicar o App na Internet

Este guia mostra como tornar seu app Node.js acessível publicamente na internet.

## 📋 Opções de Hospedagem

### 🟢 Opções Gratuitas (Recomendadas para começar)
1. **Railway** - Mais fácil, deploy automático
2. **Render** - Gratuito, fácil de usar
3. **Vercel** - Ótimo para frontend
4. **Heroku** - Clássico, mas limitado no plano gratuito

### 💰 Opções Pagas (Para produção)
1. **DigitalOcean** - VPS barato ($5/mês)
2. **AWS** - Escalável, complexo
3. **Google Cloud** - Similar ao AWS
4. **Azure** - Microsoft Cloud

---

## 🚂 Opção 1: Railway (Mais Fácil - Recomendado)

### Passo 1: Criar Conta
1. Acesse: https://railway.app/
2. Clique em "Start a New Project"
3. Faça login com GitHub

### Passo 2: Conectar Repositório
1. Selecione "Deploy from GitHub repo"
2. Escolha seu repositório
3. Selecione a pasta `nodejs-app`

### Passo 3: Configurar Variáveis
1. Vá em "Variables"
2. Adicione:
   ```
   FOOTBALL_DATA_API_KEY=sua_chave_aqui
   PORT=3000
   ```

### Passo 4: Configurar Build
Railway detecta automaticamente Node.js, mas você pode configurar:

**Settings → Build Command:**
```bash
npm install
```

**Settings → Start Command:**
```bash
npm start
```

### Passo 5: Obter URL
1. Railway gera uma URL automaticamente
2. Exemplo: `https://seu-app.up.railway.app`
3. Você pode configurar um domínio customizado depois

### ✅ Pronto!
Seu app estará online em poucos minutos!

---

## 🎨 Opção 2: Render (Gratuito e Fácil)

### Passo 1: Criar Conta
1. Acesse: https://render.com/
2. Faça login com GitHub

### Passo 2: Criar Web Service
1. Clique em "New +" → "Web Service"
2. Conecte seu repositório GitHub
3. Selecione a pasta `nodejs-app`

### Passo 3: Configurar
- **Name:** `football-ligas` (ou o nome que quiser)
- **Environment:** `Node`
- **Build Command:** `npm install`
- **Start Command:** `npm start`
- **Plan:** Free

### Passo 4: Variáveis de Ambiente
Na seção "Environment Variables", adicione:
```
FOOTBALL_DATA_API_KEY=sua_chave_aqui
PORT=3000
```

### Passo 5: Deploy
1. Clique em "Create Web Service"
2. Aguarde o deploy (5-10 minutos)
3. Render gera uma URL: `https://seu-app.onrender.com`

### ⚠️ Nota sobre Render Free
- O serviço "dorme" após 15 minutos de inatividade
- Primeira requisição pode demorar ~30 segundos (wake up)
- Para produção, considere plano pago

---

## 🟣 Opção 3: Heroku (Clássico)

### Passo 1: Instalar Heroku CLI
```bash
# Windows: Baixe de https://devcenter.heroku.com/articles/heroku-cli
# Linux/Mac:
curl https://cli-assets.heroku.com/install.sh | sh
```

### Passo 2: Login
```bash
heroku login
```

### Passo 3: Criar App
```bash
cd nodejs-app
heroku create seu-app-nome
```

### Passo 4: Configurar Variáveis
```bash
heroku config:set FOOTBALL_DATA_API_KEY=sua_chave_aqui
heroku config:set PORT=3000
```

### Passo 5: Deploy
```bash
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

### Passo 6: Abrir App
```bash
heroku open
```

### ⚠️ Nota sobre Heroku
- Plano gratuito foi descontinuado
- Precisa de cartão de crédito (mesmo no plano gratuito)
- Alternativas gratuitas: Railway, Render

---

## 💻 Opção 4: VPS (DigitalOcean - $5/mês)

### Passo 1: Criar Droplet
1. Acesse: https://www.digitalocean.com/
2. Crie uma conta
3. Crie um Droplet:
   - **OS:** Ubuntu 22.04
   - **Plan:** $5/mês (Basic)
   - **Region:** Escolha o mais próximo

### Passo 2: Conectar via SSH
```bash
ssh root@seu-ip
```

### Passo 3: Instalar Node.js
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
node --version
```

### Passo 4: Instalar PM2 (Gerenciador de Processos)
```bash
sudo npm install -g pm2
```

### Passo 5: Clonar e Configurar App
```bash
# Instalar Git
sudo apt-get install git

# Clonar repositório (ou fazer upload)
git clone seu-repositorio.git
cd nodejs-app

# Instalar dependências
npm install

# Criar .env
nano .env
# Adicione:
# FOOTBALL_DATA_API_KEY=sua_chave
# PORT=3000
```

### Passo 6: Iniciar com PM2
```bash
pm2 start server.js --name football-ligas
pm2 save
pm2 startup
```

### Passo 7: Configurar Firewall
```bash
sudo ufw allow 3000
sudo ufw enable
```

### Passo 8: Configurar Nginx (Proxy Reverso)
```bash
sudo apt-get install nginx
sudo nano /etc/nginx/sites-available/default
```

Adicione:
```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
sudo nginx -t
sudo systemctl restart nginx
```

### Passo 9: Configurar Domínio (Opcional)
1. Configure DNS do seu domínio para apontar para o IP do servidor
2. Adicione certificado SSL (Let's Encrypt):
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d seu-dominio.com
```

---

## 🔒 Configurar HTTPS (SSL)

### Com Let's Encrypt (Gratuito)

#### No VPS:
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d seu-dominio.com
```

#### No Railway/Render:
- Geralmente já vem com HTTPS automático
- Configure domínio customizado nas configurações

---

## 📱 Atualizar App Android

Depois de publicar, atualize o app Android:

### Editar `MainActivity.java`:
```java
// Substitua pela URL do seu servidor
private static final String APP_URL = "https://seu-app.railway.app";
// ou
private static final String APP_URL = "https://seu-app.onrender.com";
// ou
private static final String APP_URL = "https://seu-dominio.com";
```

---

## ✅ Checklist de Deploy

### Antes de Publicar:
- [ ] Testar localmente (`npm start`)
- [ ] Verificar se `.env` não está no Git (já está no `.gitignore`)
- [ ] Configurar variáveis de ambiente no serviço
- [ ] Verificar se a porta está correta

### Depois de Publicar:
- [ ] Testar URL no navegador
- [ ] Verificar se HTTPS funciona
- [ ] Testar API endpoints
- [ ] Atualizar URL no app Android
- [ ] Testar app Android com URL de produção

---

## 🐛 Troubleshooting

### App não inicia
- Verifique logs do serviço (Railway/Render/Heroku)
- Verifique se variáveis de ambiente estão configuradas
- Verifique se a porta está correta

### Erro 404
- Verifique se o servidor está rodando
- Verifique se a URL está correta
- Verifique configurações de roteamento

### Erro de CORS
- O servidor já tem CORS habilitado
- Se ainda houver problemas, verifique `server.js` linha 12

### Timeout no Render
- Render Free tem timeout de 15 minutos
- Primeira requisição após inatividade demora ~30s
- Considere upgrade para plano pago

---

## 🎯 Recomendações

### Para Testes/Desenvolvimento:
- ✅ **Railway** - Mais fácil, deploy rápido
- ✅ **Render** - Gratuito, fácil

### Para Produção:
- ✅ **Railway** - Plano pago ($5/mês)
- ✅ **DigitalOcean** - VPS completo ($5/mês)
- ✅ **Render** - Plano pago ($7/mês)

### Para Escala:
- ✅ **AWS** - EC2, Elastic Beanstalk
- ✅ **Google Cloud** - App Engine, Cloud Run
- ✅ **Azure** - App Service

---

## 📝 Exemplo de Deploy Rápido (Railway)

```bash
# 1. Criar conta no Railway
# 2. Conectar GitHub
# 3. Selecionar repositório e pasta nodejs-app
# 4. Adicionar variável: FOOTBALL_DATA_API_KEY
# 5. Deploy automático!
# 6. Copiar URL gerada
# 7. Atualizar MainActivity.java com a URL
```

---

## 🔗 Links Úteis

- **Railway:** https://railway.app/
- **Render:** https://render.com/
- **Heroku:** https://www.heroku.com/
- **DigitalOcean:** https://www.digitalocean.com/
- **Let's Encrypt:** https://letsencrypt.org/

---

## 💡 Dica Final

Para começar rapidamente, use **Railway** ou **Render**:
- ✅ Gratuito
- ✅ Deploy automático
- ✅ HTTPS incluído
- ✅ Fácil de configurar
- ✅ Sem necessidade de servidor próprio

Basta conectar seu GitHub e configurar as variáveis de ambiente!

