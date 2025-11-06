# ⚽ Futebol Ligas Dashboard

Dashboard interativo de futebol com análise de probabilidades e destaque de confrontos Top-3 vs Bottom-3.

## 🎯 Funcionalidades

- ✅ Dashboard interativo de múltiplas ligas
- ✅ Cálculo de probabilidades (Bradley-Terry)
- ✅ Destaque de confrontos Top-3 vs Bottom-3
- ✅ Escudos dos times
- ✅ Download de dados em CSV
- ✅ Interface moderna e responsiva
- ✅ App Android nativo

## 📁 Estrutura do Projeto

```
Ligas/
├── nodejs-app/          # Aplicação Node.js (backend + frontend)
├── android-app/         # App Android nativo
├── streamlit_app.py     # Versão Streamlit (legado)
├── football_top_vs_bottom.py  # Script Python CLI
└── README.md            # Este arquivo
```

## 🚀 Início Rápido

### Node.js App (Recomendado)

```bash
cd nodejs-app
npm install
# Crie .env com FOOTBALL_DATA_API_KEY
npm start
```

Acesse: http://localhost:3000

### App Android

1. Abra `android-app` no Android Studio
2. Configure a URL do servidor em `MainActivity.java`
3. Execute o app

## 📚 Documentação

### Node.js
- `nodejs-app/README.md` - Documentação completa
- `nodejs-app/COMO_TESTAR.md` - Como testar
- `nodejs-app/COMO_PUBLICAR_NA_INTERNET.md` - Deploy

### Android
- `android-app/README.md` - Documentação do app
- `android-app/COMO_TESTAR.md` - Como testar
- `QUICK_START_ANDROID.md` - Início rápido

### Configuração
- `COMO_OBTER_API_KEY.md` - Como obter API Key
- `ONDE_CONFIGURAR_API_KEY.md` - Onde configurar

### Deploy
- `PUBLICAR_APP.md` - Como publicar na internet
- `nodejs-app/DEPLOY_RAPIDO.md` - Deploy rápido

## 🔑 API Key

Você precisa de uma API Key do [football-data.org](https://www.football-data.org/):
1. Crie uma conta gratuita
2. Obtenha sua API Token
3. Configure no `.env` ou variável de ambiente

Veja `COMO_OBTER_API_KEY.md` para instruções detalhadas.

## 🌐 Deploy

Para publicar na internet, veja:
- `PUBLICAR_APP.md` - Guia rápido
- `nodejs-app/COMO_PUBLICAR_NA_INTERNET.md` - Guia completo

**Opções recomendadas:**
- Railway (mais fácil) - https://railway.app/
- Render (gratuito) - https://render.com/

## 📱 App Android

O app Android carrega o dashboard em um WebView nativo.

**Configurar URL:**
- Edite `android-app/app/src/main/java/com/ligas/football/MainActivity.java`
- Altere `APP_URL` para sua URL de produção

## 🛠️ Tecnologias

- **Backend:** Node.js + Express
- **Frontend:** HTML/CSS/JavaScript
- **Mobile:** Android (Java/Kotlin)
- **API:** football-data.org v4

## 📄 Licença

MIT

## 👤 Autor

Bruno Bronks

## 🔗 Links

- [football-data.org](https://www.football-data.org/)
- [Documentação API](https://www.football-data.org/documentation)

