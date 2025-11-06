# 🔧 Solução: "npm: command not found"

## ❌ Problema

O Railway não estava detectando Node.js porque o `package.json` estava apenas em `nodejs-app/`, não na raiz.

## ✅ Solução Aplicada

Criamos um `package.json` na **raiz do projeto** que:
1. Faz o Railway detectar Node.js automaticamente
2. Define scripts que entram em `nodejs-app/` e executam os comandos

### O que foi feito:

1. ✅ Criado `package.json` na raiz
2. ✅ Scripts configurados para usar `nodejs-app/`
3. ✅ `railway.json` atualizado para usar `npm start` (que já aponta para nodejs-app)

## 🚀 Próximos Passos

1. **Faça push:**
   ```bash
   git push
   ```

2. **No Railway, configure:**
   - **Build Command:** Deixe vazio ou `npm run build` (já configurado no package.json)
   - **Start Command:** `npm start` (já configurado)

3. **Variáveis de Ambiente:**
   - Adicione `FOOTBALL_DATA_API_KEY`

4. **Faça novo deploy**

## 📝 Como Funciona Agora

- Railway detecta `package.json` na raiz → Instala Node.js automaticamente
- `npm run build` → Executa `cd nodejs-app && npm install`
- `npm start` → Executa `cd nodejs-app && npm start`

---

## ✅ Deve Funcionar Agora!

O Railway vai:
1. Detectar Node.js (por causa do package.json na raiz)
2. Instalar Node.js e npm
3. Executar `npm run build` (que instala dependências em nodejs-app)
4. Executar `npm start` (que inicia o servidor em nodejs-app)

