# 🔧 Solução: Erro Nixpacks "undefined variable 'npm'"

## ❌ Problema

O erro ocorre porque o `nixpacks.toml` estava tentando instalar `npm` como pacote separado, mas `npm` já vem incluído com `nodejs-18_x`.

## ✅ Solução

### Opção 1: Configurar no Dashboard (Recomendado)

Removemos o `nixpacks.toml` problemático. Configure manualmente no Railway:

1. **Build Command:**
   - Vá em **Settings** → **Build**
   - Clique em **"+ Build Command"**
   - Digite: `cd nodejs-app && npm install`

2. **Start Command:**
   - Vá em **Settings** → **Deploy**
   - Configure: `cd nodejs-app && npm start`

3. **Variáveis:**
   - Adicione `FOOTBALL_DATA_API_KEY` em **Variables**

### Opção 2: Usar railway.json

O arquivo `railway.json` foi atualizado e está correto. Faça push:

```bash
git push
```

O Railway deve detectar automaticamente.

---

## 📝 O que foi corrigido

- ❌ Removido `nixpacks.toml` (causava erro)
- ✅ `railway.json` atualizado (sem buildCommand, será configurado no dashboard)
- ✅ Comandos devem ser configurados manualmente no Railway

---

## 🚀 Próximos Passos

1. Configure os comandos no dashboard do Railway
2. Adicione a variável `FOOTBALL_DATA_API_KEY`
3. Faça um novo deploy
4. Deve funcionar agora!

