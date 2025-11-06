# ⚽ Futebol Ligas - Node.js App

Aplicação Node.js que substitui o Streamlit, fornecendo dashboard de futebol com probabilidades e análise Top-3 vs Bottom-3.

## 🚀 Início Rápido

### 1. Instalar Dependências

```bash
npm install
```

### 2. Configurar API Key

Crie um arquivo `.env` na raiz do projeto:

```env
FOOTBALL_DATA_API_KEY=sua_chave_aqui
PORT=3000
```

Ou configure via variável de ambiente:

```bash
# Windows PowerShell
$env:FOOTBALL_DATA_API_KEY="sua_chave_aqui"

# Linux/Mac
export FOOTBALL_DATA_API_KEY="sua_chave_aqui"
```

### 3. Iniciar o Servidor

```bash
# Modo produção
npm start

# Modo desenvolvimento (com auto-reload)
npm run dev
```

O servidor estará disponível em: `http://localhost:3000`

## 🧪 Como Testar

Para instruções detalhadas de testes, consulte:
- `COMO_TESTAR.md` - Guia completo de testes
- `TESTAR_RAPIDO.md` - Teste rápido em 3 passos

## 📋 Funcionalidades

- ✅ Dashboard interativo de futebol
- ✅ Múltiplas ligas (Bundesliga, Premier League, Ligue 1, Eredivisie, Brasileirão A, La Liga, Champions League)
- ✅ Cálculo de probabilidades (Bradley-Terry)
- ✅ Destaque de confrontos Top-3 vs Bottom-3
- ✅ Download de dados em CSV
- ✅ Cache inteligente (60s TTL)
- ✅ Retry automático em caso de rate limit

## 🔧 Configuração

### Porta do Servidor

Por padrão, o servidor roda na porta 3000. Para alterar:

1. Defina `PORT` no arquivo `.env`
2. Ou use variável de ambiente: `PORT=8080 npm start`

### API Key

A API key pode ser configurada de 3 formas:

1. **Arquivo `.env`** (recomendado para desenvolvimento)
2. **Variável de ambiente** `FOOTBALL_DATA_API_KEY`
3. **Interface web** (digite no campo do formulário)

## 📱 Integração com App Android

Para usar com o app Android, configure a URL em `MainActivity.java`:

```java
// Para desenvolvimento local (emulador)
private static final String STREAMLIT_URL = "http://10.0.2.2:3000";

// Para dispositivo físico (mesma rede)
private static final String STREAMLIT_URL = "http://192.168.1.100:3000";

// Para produção
private static final String STREAMLIT_URL = "https://seu-servidor.com";
```

## 🌐 Deploy (Publicar na Internet)

Para instruções detalhadas de como publicar o app na internet, consulte:
- **`COMO_PUBLICAR_NA_INTERNET.md`** - Guia completo com todas as opções
- **`DEPLOY_RAPIDO.md`** - Deploy rápido em 5 minutos

### Opções Recomendadas:

1. **Railway** (Mais fácil) - https://railway.app/
   - Deploy automático via GitHub
   - Gratuito para começar
   - HTTPS incluído

2. **Render** (Gratuito) - https://render.com/
   - Deploy automático
   - Plano gratuito disponível
   - HTTPS incluído

3. **Heroku** (Clássico)
   - Precisa de cartão de crédito
   - Plano gratuito limitado

4. **VPS** (DigitalOcean - $5/mês)
   - Controle total
   - Para usuários avançados

## 📁 Estrutura do Projeto

```
nodejs-app/
├── server.js          # Servidor Express e lógica de negócio
├── package.json       # Dependências e scripts
├── .env.example       # Exemplo de configuração
├── public/
│   ├── index.html     # Interface web
│   ├── styles.css     # Estilos
│   └── app.js         # JavaScript do frontend
└── README.md          # Este arquivo
```

## 🔌 API Endpoints

### `POST /api/league-data`

Busca dados de uma liga específica.

**Request Body:**
```json
{
  "token": "sua_api_key",
  "leagueCode": "PL",
  "dateFrom": "2024-01-01",
  "dateTo": "2024-01-31",
  "daysAhead": 10
}
```

**Response:**
```json
{
  "standings": [...],
  "strengths": [...],
  "fixtures": [...],
  "probabilities": [...]
}
```

### `POST /api/clear-cache`

Limpa o cache do servidor.

### `GET /health`

Health check do servidor.

## 🐛 Troubleshooting

### Erro: "API token é obrigatório"

- Verifique se a API key está configurada no `.env` ou no campo do formulário
- Certifique-se de que o arquivo `.env` está na raiz do projeto

### Erro: "ECONNREFUSED" ou "Network Error"

- Verifique se o servidor está rodando: `npm start`
- Verifique se a porta está correta
- Para app Android, use `10.0.2.2` (emulador) ou IP do computador (dispositivo físico)

### Rate Limit (429)

- O app tem retry automático com backoff exponencial
- Cache de 60s reduz chamadas à API
- Aguarde alguns segundos e tente novamente

## 📝 Notas

- Cache em memória (não persiste entre reinicializações)
- Para produção, considere usar Redis para cache distribuído
- HTTPS é recomendado para produção
- Configure CORS adequadamente se necessário

## 🔄 Migração do Streamlit

Este app Node.js é uma substituição completa do Streamlit, mantendo todas as funcionalidades:

- ✅ Mesma lógica de cálculo de probabilidades
- ✅ Mesmas ligas suportadas
- ✅ Interface similar
- ✅ Download de CSV
- ✅ Cache e retry

Vantagens:
- ✅ Mais leve (sem Python/Streamlit)
- ✅ Melhor para mobile (menor overhead)
- ✅ Mais fácil de deployar
- ✅ API REST separada do frontend

