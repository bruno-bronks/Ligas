# 🔄 Migração de Streamlit para Node.js

Este guia explica como migrar do Streamlit (Python) para a versão Node.js.

## ✅ O que foi criado

### Estrutura Node.js Completa

```
nodejs-app/
├── server.js          # Servidor Express com toda lógica
├── package.json       # Dependências Node.js
├── public/
│   ├── index.html     # Interface web
│   ├── styles.css     # Estilos CSS
│   └── app.js         # JavaScript frontend
└── README.md          # Documentação
```

## 🚀 Como Usar

### 1. Instalar Node.js

Baixe e instale Node.js (versão 16+):
- https://nodejs.org/

### 2. Instalar Dependências

```bash
cd nodejs-app
npm install
```

### 3. Configurar API Key

Crie um arquivo `.env`:

```env
FOOTBALL_DATA_API_KEY=sua_chave_aqui
PORT=3000
```

Ou use variável de ambiente:

```bash
# Windows PowerShell
$env:FOOTBALL_DATA_API_KEY="sua_chave"

# Linux/Mac
export FOOTBALL_DATA_API_KEY="sua_chave"
```

### 4. Iniciar o Servidor

```bash
# Modo produção
npm start

# Modo desenvolvimento (com auto-reload)
npm run dev
```

O app estará disponível em: `http://localhost:3000`

## 📱 Atualizar App Android

O app Android já foi atualizado! A URL padrão agora aponta para a porta 3000 (Node.js) em vez de 8501 (Streamlit).

### Para desenvolvimento local:

**Emulador Android:**
```java
private static final String APP_URL = "http://10.0.2.2:3000";
```

**Dispositivo físico:**
```java
private static final String APP_URL = "http://192.168.1.100:3000";
```
(Substitua pelo IP do seu computador)

### Para produção:

```java
private static final String APP_URL = "https://seu-servidor.com";
```

## 🔄 Diferenças Principais

### Streamlit (Python)
- Porta: 8501
- Framework: Streamlit
- Linguagem: Python
- Dependências: pandas, numpy, requests, streamlit

### Node.js
- Porta: 3000
- Framework: Express
- Linguagem: JavaScript
- Dependências: express, axios, cors, dotenv

## ✨ Vantagens do Node.js

1. **Mais leve**: Sem necessidade de Python/Streamlit
2. **Melhor para mobile**: Menor overhead, mais rápido
3. **API REST separada**: Frontend e backend desacoplados
4. **Fácil deploy**: Funciona em qualquer plataforma Node.js
5. **Mesma funcionalidade**: Todas as features do Streamlit mantidas

## 🎯 Funcionalidades Mantidas

- ✅ Dashboard interativo
- ✅ Múltiplas ligas
- ✅ Cálculo de probabilidades (Bradley-Terry)
- ✅ Destaque Top-3 vs Bottom-3
- ✅ Download CSV
- ✅ Cache inteligente
- ✅ Retry automático

## 🌐 Deploy

### Opção 1: Heroku

```bash
heroku create seu-app
heroku config:set FOOTBALL_DATA_API_KEY=sua_chave
git push heroku main
```

### Opção 2: Railway

1. Conecte GitHub
2. Configure `FOOTBALL_DATA_API_KEY`
3. Deploy automático!

### Opção 3: VPS

```bash
npm install -g pm2
pm2 start server.js --name football-ligas
pm2 save
pm2 startup
```

## 📝 Próximos Passos

1. ✅ Teste o servidor Node.js localmente
2. ✅ Atualize a URL no app Android
3. ✅ Teste no emulador/dispositivo
4. ✅ Faça deploy em produção
5. ✅ Atualize a URL do app Android para produção

## 🐛 Troubleshooting

### Porta 3000 já em uso?

Altere no `.env`:
```env
PORT=3001
```

E atualize o app Android para usar a nova porta.

### App Android não carrega?

- Verifique se o servidor Node.js está rodando
- Verifique a URL no `MainActivity.java`
- Para emulador, use `10.0.2.2:3000`
- Para dispositivo físico, use o IP do computador

### Erro de API Key?

- Verifique se está configurada no `.env`
- Ou digite no campo do formulário web

## 📚 Documentação

- `nodejs-app/README.md` - Documentação completa do Node.js
- `android-app/README.md` - Documentação do app Android
- `android-app/COMO_TESTAR.md` - Como testar o app

