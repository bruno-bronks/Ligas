# Sistema de Múltiplas APIs

Este sistema permite usar múltiplas APIs de futebol com fallback automático. Se uma API falhar, o sistema tenta automaticamente a próxima API configurada.

## Estrutura

```
apis/
├── config.js          # Configuração das APIs disponíveis
├── manager.js         # Gerenciador que coordena as APIs
├── football-data.js   # Adaptador para football-data.org
├── footystats.js      # Adaptador para FootyStats (template)
└── README.md          # Esta documentação
```

## Como Funciona

1. **Configuração**: APIs são configuradas em `config.js` com prioridade
2. **Seleção**: O manager encontra APIs que suportam a liga solicitada
3. **Tentativa**: Tenta cada API em ordem de prioridade
4. **Fallback**: Se uma API falhar, tenta a próxima automaticamente
5. **Retorno**: Retorna dados da primeira API que funcionar

## Adicionar uma Nova API

### 1. Criar o Adaptador

Crie um novo arquivo em `apis/` (ex: `apis/nova-api.js`):

```javascript
const axios = require('axios');

class NovaAPIAdapter {
  constructor() {
    this.name = 'nova-api';
    this.baseUrl = 'https://api.exemplo.com';
    this.leagueMapping = {
      'RFPL': 123, // Mapear códigos de liga para IDs da API
      'UPL': 124
    };
  }

  getLeagueCode(leagueCode) {
    return this.leagueMapping[leagueCode] || leagueCode;
  }

  supportsLeague(leagueCode) {
    return this.leagueMapping.hasOwnProperty(leagueCode);
  }

  async getStandings(token, leagueCode) {
    const apiCode = this.getLeagueCode(leagueCode);
    const url = `${this.baseUrl}/standings/${apiCode}`;
    
    const response = await axios.get(url, {
      headers: token ? { 'Authorization': `Bearer ${token}` } : {},
      timeout: 30000
    });

    // Converter formato da API para formato padrão
    return (response.data.data || []).map(row => ({
      position: row.position,
      team_id: row.team_id,
      team: row.team,
      tla: row.tla || '',
      played: row.played || 0,
      won: row.won || 0,
      draw: row.draw || 0,
      lost: row.lost || 0,
      gf: row.gf || 0,
      ga: row.ga || 0,
      gd: row.gd || 0,
      points: row.points || 0,
      form: row.form || ''
    }));
  }

  async getUpcomingMatches(token, leagueCode, dateFrom, dateTo, daysAhead) {
    // Implementar similar ao getStandings
    // ...
  }
}

module.exports = new NovaAPIAdapter();
```

### 2. Registrar no Config

Adicione a nova API em `apis/config.js`:

```javascript
{
  name: 'nova-api',
  enabled: true,
  priority: 2, // Ordem de tentativa (menor = maior prioridade)
  adapter: require('./nova-api'),
  leagues: {
    'RFPL': 'Russian Premier League',
    'UPL': 'Ukrainian Premier League'
  }
}
```

### 3. Testar

O sistema tentará automaticamente a nova API quando necessário.

## Formato Padrão de Dados

### Standings (Classificação)

```javascript
[
  {
    position: 1,
    team_id: 123,
    team: "Nome do Time",
    tla: "TLA",
    played: 10,
    won: 7,
    draw: 2,
    lost: 1,
    gf: 20,
    ga: 10,
    gd: 10,
    points: 23,
    form: "WWWDL"
  }
]
```

### Matches (Jogos)

```javascript
[
  {
    match_id: 456,
    utcDate: "2024-01-15T20:00:00Z",
    status: "SCHEDULED",
    matchday: 5,
    home_id: 123,
    home: "Time Casa",
    home_tla: "TCA",
    away_id: 124,
    away: "Time Visitante",
    away_tla: "TVS"
  }
]
```

## Configuração de APIs

### Habilitar/Desabilitar APIs

Em `config.js`, altere `enabled: true/false` para cada API.

### Prioridade

Ajuste `priority` para controlar a ordem de tentativa:
- Menor número = maior prioridade
- APIs com prioridade 1 são tentadas primeiro

## Logs

O sistema registra no console:
- Qual API está sendo tentada
- Sucesso ou falha de cada tentativa
- Qual API foi usada com sucesso

## Exemplo de Uso

```javascript
const apiManager = require('./apis/manager');

// Obter standings - tenta todas as APIs até uma funcionar
const result = await apiManager.getStandings(token, 'RFPL');
console.log(`Dados obtidos de: ${result.source}`);
console.log(`Standings:`, result.data);

// Obter jogos
const matches = await apiManager.getUpcomingMatches(token, 'UPL', null, null, 10);
```

## Notas

- Cada adaptador deve converter o formato da sua API para o formato padrão
- O sistema mantém compatibilidade com o código antigo (fallback)
- APIs são tentadas em ordem até uma funcionar
- Se todas falharem, o sistema usa o método antigo como último recurso

