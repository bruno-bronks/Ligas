# 📤 Como Fazer Push para GitHub

## 📍 Onde Fazer Push

O `git push` deve ser feito no **diretório raiz do projeto** (`Ligas`), **NÃO** em `nodejs-app/`.

## ✅ Comandos Corretos

### 1. Certifique-se de estar na raiz

```bash
# Você deve estar aqui:
C:\Users\user\Documents\Bruno\Projetos\Ligas

# NÃO aqui:
C:\Users\user\Documents\Bruno\Projetos\Ligas\nodejs-app
```

### 2. Verificar se está na raiz

```bash
# Deve mostrar arquivos como:
# - package.json (raiz)
# - railway.json
# - README.md
# - nodejs-app/
# - android-app/
dir
```

### 3. Fazer Push

```bash
# Adicionar mudanças
git add .

# Commit
git commit -m "Descrição das mudanças"

# Push para GitHub
git push
```

## 🔍 Verificar Repositório

```bash
# Ver remote configurado
git remote -v

# Deve mostrar algo como:
# origin  https://github.com/bruno-bronks/Ligas.git
```

## ⚠️ Importante

- ✅ **Faça push na raiz** (`Ligas/`)
- ❌ **NÃO faça push em** `nodejs-app/` (não é um repositório Git separado)
- ✅ Todo o projeto (incluindo `nodejs-app/` e `android-app/`) será enviado

## 📝 Estrutura

```
Ligas/                    ← AQUI você faz git push
├── .git/                 ← Repositório Git está aqui
├── package.json          ← Criado para Railway
├── railway.json
├── nodejs-app/           ← Parte do projeto
└── android-app/          ← Parte do projeto
```

## 🚀 Depois do Push

1. O Railway vai detectar automaticamente as mudanças
2. Vai fazer um novo deploy
3. Deve funcionar agora!

