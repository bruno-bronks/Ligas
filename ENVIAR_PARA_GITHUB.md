# 📤 Como Enviar para o GitHub

## 🚀 Passo a Passo

### 1. Criar Repositório no GitHub

1. Acesse: https://github.com/bruno-bronks
2. Clique em "New repository" (ou "+" → "New repository")
3. Configure:
   - **Name:** `Ligas` (ou o nome que preferir)
   - **Description:** "Dashboard de Futebol - Top-3 vs Bottom-3"
   - **Visibility:** Public ou Private (sua escolha)
   - **NÃO** marque "Initialize with README" (já temos um)
4. Clique em "Create repository"

### 2. Inicializar Git Localmente

Abra o terminal na pasta do projeto e execute:

```bash
# Inicializar repositório Git
git init

# Adicionar todos os arquivos
git add .

# Fazer commit inicial
git commit -m "Initial commit: Dashboard de Futebol com Node.js e Android"
```

### 3. Conectar ao GitHub

```bash
# Adicionar remote (substitua SEU-REPOSITORIO pelo nome que você escolheu)
git remote add origin https://github.com/bruno-bronks/SEU-REPOSITORIO.git

# Verificar se foi adicionado
git remote -v
```

### 4. Enviar para o GitHub

```bash
# Enviar para o GitHub
git branch -M main
git push -u origin main
```

Você será solicitado a fazer login no GitHub.

### 5. Verificar

Acesse: https://github.com/bruno-bronks/SEU-REPOSITORIO

Seu código deve estar lá! 🎉

---

## 🔐 Autenticação GitHub

### Opção 1: Personal Access Token (Recomendado)

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. "Generate new token"
3. Marque: `repo` (acesso completo aos repositórios)
4. Copie o token
5. Use o token como senha quando o Git pedir

### Opção 2: GitHub CLI

```bash
# Instalar GitHub CLI
# Windows: winget install GitHub.cli
# Mac: brew install gh
# Linux: apt install gh

# Login
gh auth login

# Depois pode usar normalmente
git push
```

### Opção 3: SSH (Avançado)

```bash
# Gerar chave SSH
ssh-keygen -t ed25519 -C "seu-email@example.com"

# Copiar chave pública
cat ~/.ssh/id_ed25519.pub

# Adicionar no GitHub: Settings → SSH and GPG keys → New SSH key

# Usar URL SSH
git remote set-url origin git@github.com:bruno-bronks/SEU-REPOSITORIO.git
```

---

## ⚠️ Arquivos que NÃO serão enviados

O arquivo `.gitignore` já está configurado para ignorar:
- ✅ `.env` (com API keys)
- ✅ `node_modules/`
- ✅ Arquivos compilados
- ✅ Logs e temporários

**Importante:** Nunca commite arquivos `.env` com suas chaves!

---

## 🔄 Atualizar Repositório (Futuro)

Depois do primeiro push, para atualizar:

```bash
git add .
git commit -m "Descrição das mudanças"
git push
```

---

## 📝 Comandos Úteis

```bash
# Ver status
git status

# Ver histórico
git log

# Ver diferenças
git diff

# Criar nova branch
git checkout -b nova-feature

# Voltar para main
git checkout main
```

---

## 🆘 Problemas Comuns

### Erro: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/bruno-bronks/SEU-REPOSITORIO.git
```

### Erro: "failed to push"
- Verifique se você tem permissão no repositório
- Verifique se o repositório existe no GitHub
- Tente fazer login novamente

### Erro: "authentication failed"
- Use Personal Access Token em vez de senha
- Ou configure SSH

---

## ✅ Checklist

- [ ] Repositório criado no GitHub
- [ ] Git inicializado localmente
- [ ] `.gitignore` configurado
- [ ] Remote adicionado
- [ ] Primeiro commit feito
- [ ] Push realizado com sucesso
- [ ] Código visível no GitHub

---

## 🎯 Próximos Passos

Depois de enviar para o GitHub:

1. **Deploy Automático:**
   - Railway/Render podem fazer deploy automático do GitHub
   - Conecte o repositório e configure

2. **Colaboradores:**
   - Adicione colaboradores no GitHub
   - Settings → Collaborators

3. **Issues e Pull Requests:**
   - Use Issues para bugs e features
   - Use Pull Requests para contribuições

---

## 📚 Mais Informações

- [Documentação Git](https://git-scm.com/doc)
- [GitHub Docs](https://docs.github.com/)
- [GitHub CLI](https://cli.github.com/)

