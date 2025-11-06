# 🚀 Comandos para Enviar para GitHub

## ⚡ Comandos Rápidos

Execute estes comandos na ordem:

### 1. Criar Repositório no GitHub Primeiro!

1. Acesse: https://github.com/bruno-bronks
2. Clique em "New repository"
3. Nome: `Ligas` (ou outro nome)
4. **NÃO** marque "Initialize with README"
5. Clique em "Create repository"

### 2. Conectar e Enviar

```bash
# Adicionar remote (SUBSTITUA SEU-REPOSITORIO pelo nome que você escolheu)
git remote add origin https://github.com/bruno-bronks/SEU-REPOSITORIO.git

# Renomear branch para main
git branch -M main

# Enviar para GitHub
git push -u origin main
```

### 3. Autenticação

Quando pedir usuário/senha:
- **Usuário:** bruno-bronks
- **Senha:** Use um Personal Access Token (não sua senha do GitHub)

**Como criar token:**
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. "Generate new token"
3. Marque: `repo`
4. Copie o token e use como senha

---

## ✅ Pronto!

Seu código estará em: https://github.com/bruno-bronks/SEU-REPOSITORIO

---

## 📝 Comandos Já Executados

✅ `git init` - Repositório inicializado
✅ `git add .` - Arquivos adicionados
✅ `git commit` - Commit inicial feito

**Falta apenas:**
- Criar repositório no GitHub
- Adicionar remote
- Fazer push

---

## 🔄 Atualizar no Futuro

```bash
git add .
git commit -m "Descrição das mudanças"
git push
```

