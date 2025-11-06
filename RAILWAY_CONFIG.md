# 🚂 Configuração Railway - Solução

O Railway está analisando a raiz do projeto, mas o app Node.js está em `nodejs-app/`.

## ✅ Solução 1: Configurar no Railway (Recomendado)

### No Dashboard do Railway:

1. Vá em **Settings** do seu projeto
2. Procure por **"Root Directory"** ou **"Working Directory"**
3. Defina: `nodejs-app`
4. Salve

### Variáveis de Ambiente:

Na seção **Variables**, adicione:
```
FOOTBALL_DATA_API_KEY=sua_chave_aqui
PORT=3000
```

### Build & Start Commands:

**Build Command:**
```bash
npm install
```

**Start Command:**
```bash
npm start
```

---

## ✅ Solução 2: Arquivos de Configuração

Já foram criados arquivos na raiz:
- `railway.json` - Configuração do Railway
- `nixpacks.toml` - Configuração do Nixpacks

O Railway deve detectar automaticamente.

---

## ✅ Solução 3: Mover arquivos (Alternativa)

Se as soluções acima não funcionarem, você pode:

1. **Criar um novo projeto Railway** apontando diretamente para a pasta `nodejs-app`
2. Ou **mover** o conteúdo de `nodejs-app/` para a raiz (não recomendado)

---

## 🔍 Verificar

Depois de configurar, o Railway deve:
1. Detectar Node.js
2. Executar `npm install` em `nodejs-app/`
3. Executar `npm start` em `nodejs-app/`

---

## 📝 Checklist

- [ ] Root Directory configurado para `nodejs-app`
- [ ] Variável `FOOTBALL_DATA_API_KEY` adicionada
- [ ] Build Command: `npm install`
- [ ] Start Command: `npm start`
- [ ] Deploy iniciado

---

## 🆘 Se ainda não funcionar

1. Verifique os logs do Railway
2. Certifique-se de que `nodejs-app/package.json` existe
3. Tente criar um novo projeto Railway apontando diretamente para `nodejs-app/`

