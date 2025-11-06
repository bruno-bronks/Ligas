# 🔧 Deploy Travado em "Running pre-deploy command"

## ❌ Problema

O deploy está travado há mais de 1 hora em "Running pre-deploy command...". Isso não é normal.

## ✅ Solução Imediata

### 1. Cancelar Deploy Travado

1. No card do deploy, clique nos **três pontos (...)** no canto superior direito
2. Selecione **"Cancel"** ou **"Stop"**
3. Isso vai parar o deploy travado

### 2. Verificar Logs

1. Clique em **"View logs"** no card do deploy
2. Veja onde o deploy travou
3. Procure por erros ou mensagens de timeout

### 3. Verificar Configurações

1. Vá em **Settings** → **Deploy**
2. Verifique se há **"Pre-deploy Command"** configurado
3. Se houver, **remova ou corrija** o comando
4. O problema pode estar aí!

### 4. Fazer Novo Deploy

1. Após cancelar, clique em **"Redeploy"** ou **"Deploy"**
2. Monitore os logs
3. Deve completar em 2-5 minutos

## 🔍 Possíveis Causas

### Pre-deploy Command Problemático

Se você configurou um "Pre-deploy Command" em Settings → Deploy:
- Pode estar travado
- Pode ter erro
- Pode estar esperando input

**Solução:** Remova ou corrija o comando

### Build Command Muito Longo

O build pode estar travado em `npm install`.

**Solução:** 
- Verifique se `node_modules/` está no `.gitignore`
- Não envie `node_modules/` para o Git

### Recursos Insuficientes

Plano gratuito pode ter limitações.

**Solução:** Aguarde ou considere upgrade

## 📝 Checklist

- [ ] Deploy cancelado
- [ ] Logs verificados
- [ ] Pre-deploy Command removido/corrigido
- [ ] Build Command verificado
- [ ] Novo deploy iniciado
- [ ] Logs monitorados

## 🚀 Depois que Funcionar

Quando o deploy completar com sucesso:

1. **Copie a URL:** `ligas-production.up.railway.app`
2. **Atualize MainActivity.java:**
   ```java
   private static final String APP_URL = "https://ligas-production.up.railway.app";
   ```
3. **Teste no navegador:** `https://ligas-production.up.railway.app`
4. **Teste no app Android**

---

## ⚡ Ação Rápida

1. **Cancele o deploy atual** (três pontos → Cancel)
2. **Vá em Settings → Deploy**
3. **Remova qualquer "Pre-deploy Command"** se houver
4. **Faça novo deploy**
5. **Monitore os logs**

