# 🔧 Solução: Railway não encontra o app Node.js

## ❌ Problema

O Railway está analisando a raiz do projeto, mas o app Node.js está em `nodejs-app/`.

## ✅ Solução: Configurar Root Directory

### No Dashboard do Railway:

1. **Acesse seu projeto no Railway**
2. Vá em **Settings** (Configurações)
3. Procure por **"Root Directory"** ou **"Working Directory"**
4. **Defina:** `nodejs-app`
5. **Salve as alterações**

### Configurar Build e Start:

**Build Command:**
```bash
npm install
```

**Start Command:**
```bash
npm start
```

### Variáveis de Ambiente:

Na seção **Variables**, adicione:
```
FOOTBALL_DATA_API_KEY=sua_chave_aqui
PORT=3000
```

---

## ✅ Alternativa: Criar Projeto Separado

Se não conseguir configurar o Root Directory:

1. **Crie um novo projeto Railway**
2. **Conecte o mesmo repositório GitHub**
3. **Mas selecione a pasta `nodejs-app`** ao invés da raiz
4. Configure as variáveis de ambiente
5. Faça o deploy

---

## 📝 Arquivos Criados

Foram criados arquivos na raiz para ajudar:
- `railway.json` - Configuração do Railway
- `nixpacks.toml` - Configuração do Nixpacks

Mas a **melhor solução** é configurar o **Root Directory** no dashboard.

---

## 🔄 Depois de Configurar

1. Railway vai detectar Node.js
2. Vai executar `npm install` em `nodejs-app/`
3. Vai executar `npm start` em `nodejs-app/`
4. Seu app estará online!

---

## 🆘 Ainda com Problemas?

1. Verifique os logs do Railway
2. Certifique-se de que `nodejs-app/package.json` existe
3. Tente fazer um novo deploy após configurar o Root Directory

