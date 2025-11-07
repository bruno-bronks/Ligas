const express = require('express');
const axios = require('axios');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;
const API_BASE = 'https://api.football-data.org/v4';

// Middleware
app.use(cors());
app.use(express.json());

// Desabilitar cache para arquivos estáticos (HTML, CSS, JS)
app.use(express.static(path.join(__dirname, 'public'), {
  setHeaders: (res, filePath) => {
    if (filePath.endsWith('.html') || filePath.endsWith('.css') || filePath.endsWith('.js')) {
      res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
      res.setHeader('Pragma', 'no-cache');
      res.setHeader('Expires', '0');
    }
  }
}));

// Cache simples em memória (TTL 60s)
const cache = new Map();

function getCacheKey(url, params) {
  return `${url}?${JSON.stringify(params || {})}`;
}

function getCached(key) {
  const item = cache.get(key);
  if (item && Date.now() - item.timestamp < 60000) {
    return item.data;
  }
  cache.delete(key);
  return null;
}

function setCache(key, data) {
  cache.set(key, { data, timestamp: Date.now() });
}

// Função de requisição com retry
async function requestWithRetry(url, token, params = null, maxRetries = 4, backoff = 1.7) {
  const headers = token ? { 'X-Auth-Token': token } : {};
  const cacheKey = getCacheKey(url, params);
  
  // Verificar cache
  const cached = getCached(cacheKey);
  if (cached) {
    return cached;
  }

  let lastError = null;
  
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await axios.get(url, {
        headers,
        params,
        timeout: 30000
      });

      if (response.status === 429) {
        const retryAfter = response.headers['retry-after'];
        const waitTime = retryAfter ? parseFloat(retryAfter) : Math.pow(backoff, i + 1);
        await new Promise(resolve => setTimeout(resolve, waitTime * 1000));
        continue;
      }

      if (response.status >= 400) {
        // Verificar se a resposta é HTML (página de erro)
        const contentType = response.headers['content-type'] || '';
        if (contentType.includes('text/html')) {
          lastError = new Error(`HTTP ${response.status}: A API retornou uma página de erro HTML. Verifique sua API key e o endpoint.`);
        } else {
          const errorMsg = response.data?.message || response.data?.error || 'Error';
          lastError = new Error(`HTTP ${response.status}: ${errorMsg}`);
        }
        await new Promise(resolve => setTimeout(resolve, Math.pow(backoff, i + 1) * 1000));
        continue;
      }

      const data = response.data;
      setCache(cacheKey, data);
      return data;
    } catch (error) {
      lastError = error;
      
      // Verificar se a resposta é HTML (página de erro)
      if (error.response) {
        const contentType = error.response.headers['content-type'] || '';
        if (contentType.includes('text/html')) {
          lastError = new Error(`HTTP ${error.response.status}: A API retornou uma página de erro HTML. Verifique sua API key e o endpoint.`);
        } else if (error.response.status === 429) {
          const retryAfter = error.response.headers['retry-after'];
          const waitTime = retryAfter ? parseFloat(retryAfter) : Math.pow(backoff, i + 1);
          await new Promise(resolve => setTimeout(resolve, waitTime * 1000));
          continue;
        } else if (error.response.status >= 400) {
          const errorMsg = error.response.data?.message || error.response.data?.error || `HTTP ${error.response.status}`;
          lastError = new Error(errorMsg);
        }
      }
      
      // Se não for erro 429, aguardar antes de tentar novamente
      if (error.response?.status !== 429) {
        await new Promise(resolve => setTimeout(resolve, Math.pow(backoff, i + 1) * 1000));
      }
    }
  }

  throw lastError || new Error('Falha após múltiplas tentativas de requisição');
}

// Obter standings
async function getTotalStanding(token, leagueCode) {
  const url = `${API_BASE}/competitions/${leagueCode}/standings`;
  const data = await requestWithRetry(url, token);
  
  const standings = data.standings || [];
  const tables = standings.filter(s => s.table).sort((a, b) => {
    if (a.type === 'TOTAL') return -1;
    if (b.type === 'TOTAL') return 1;
    return 0;
  });

  const rows = [];
  for (const block of tables) {
    for (const row of block.table || []) {
      const team = row.team || {};
      rows.push({
        position: row.position,
        team_id: team.id,
        team: team.name,
        tla: team.tla,
        played: row.playedGames,
        won: row.won,
        draw: row.draw,
        lost: row.lost,
        gf: row.goalsFor,
        ga: row.goalsAgainst,
        gd: row.goalDifference,
        points: row.points,
        form: row.form
      });
    }
  }

  // Para Champions League, criar ranking global
  if (leagueCode === 'CL' && rows.length > 0) {
    rows.sort((a, b) => {
      if (b.points !== a.points) return b.points - a.points;
      if (b.gd !== a.gd) return b.gd - a.gd;
      if (b.gf !== a.gf) return b.gf - a.gf;
      return a.team.localeCompare(b.team);
    });
    rows.forEach((row, idx) => {
      row.position = idx + 1;
    });
  }

  return rows;
}

// Obter próximos jogos
async function getUpcomingMatches(token, leagueCode, dateFrom = null, dateTo = null, daysAhead = 10) {
  const url = `${API_BASE}/competitions/${leagueCode}/matches`;
  
  let fromDate = dateFrom;
  let toDate = dateTo;
  
  if (!fromDate || !toDate) {
    const today = new Date();
    today.setUTCHours(0, 0, 0, 0);
    fromDate = fromDate || today.toISOString().split('T')[0];
    toDate = toDate || new Date(today.getTime() + daysAhead * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
  }

  const params = {
    status: 'SCHEDULED,TIMED',
    dateFrom: fromDate,
    dateTo: toDate
  };

  const data = await requestWithRetry(url, token, params);
  
  const rows = [];
  for (const match of data.matches || []) {
    const home = match.homeTeam || {};
    const away = match.awayTeam || {};
    rows.push({
      match_id: match.id,
      utcDate: match.utcDate,
      status: match.status,
      matchday: match.matchday,
      home_id: home.id,
      home: home.name,
      home_tla: home.tla,
      away_id: away.id,
      away: away.name,
      away_tla: away.tla,
      venue: match.venue
    });
  }

  return rows;
}

// Calcular forças das equipes
function calculateLeagueStrengths(table) {
  if (!table || table.length === 0) {
    return [];
  }

  const df = table.map(row => ({
    ...row,
    played: row.played || 0,
    ppg: row.played > 0 ? row.points / row.played : 0,
    gdg: row.played > 0 ? row.gd / row.played : 0
  }));

  // Calcular medianas para preencher NaN
  const ppgValues = df.map(r => r.ppg).filter(v => !isNaN(v) && isFinite(v));
  const medianPpg = ppgValues.length > 0 
    ? ppgValues.sort((a, b) => a - b)[Math.floor(ppgValues.length / 2)]
    : 0;

  df.forEach(row => {
    if (!isFinite(row.ppg) || isNaN(row.ppg)) row.ppg = medianPpg;
    if (!isFinite(row.gdg) || isNaN(row.gdg)) row.gdg = 0;
  });

  // Calcular z-scores
  const ppgMean = df.reduce((sum, r) => sum + r.ppg, 0) / df.length;
  const ppgStd = Math.sqrt(df.reduce((sum, r) => sum + Math.pow(r.ppg - ppgMean, 2), 0) / df.length) || 1;
  
  const gdgMean = df.reduce((sum, r) => sum + r.gdg, 0) / df.length;
  const gdgStd = Math.sqrt(df.reduce((sum, r) => sum + Math.pow(r.gdg - gdgMean, 2), 0) / df.length) || 1;

  df.forEach(row => {
    row.z_ppg = (row.ppg - ppgMean) / ppgStd;
    row.z_gdg = (row.gdg - gdgMean) / gdgStd;
    row.rating = 0.7 * row.z_ppg + 0.3 * row.z_gdg;
  });

  // Clip extremos (5% e 95%)
  const ratings = df.map(r => r.rating).sort((a, b) => a - b);
  const lowerBound = ratings[Math.floor(ratings.length * 0.05)] || ratings[0];
  const upperBound = ratings[Math.floor(ratings.length * 0.95)] || ratings[ratings.length - 1];

  return df.map(row => ({
    team_id: row.team_id,
    team: row.team,
    position: row.position,
    points: row.points,
    played: row.played,
    gd: row.gd,
    rating: Math.max(lowerBound, Math.min(upperBound, row.rating))
  }));
}

// Calcular probabilidades Bradley-Terry
function calculateBTProbabilities(homeRating, awayRating, baseDraw = 0.24, k = 1.20, homeAdv = 0.15) {
  const delta = (homeRating - awayRating) + homeAdv;
  const pHomeRaw = 1 / (1 + Math.exp(-k * delta));
  const pAwayRaw = 1 - pHomeRaw;
  const pDrawRaw = baseDraw * Math.exp(-Math.abs(delta));
  const z = pHomeRaw + pAwayRaw + pDrawRaw;
  
  return {
    pHome: pHomeRaw / z,
    pDraw: pDrawRaw / z,
    pAway: pAwayRaw / z
  };
}

// Calcular probabilidades dos jogos
function calculateMatchProbabilities(fixtures, strengths) {
  if (!fixtures || fixtures.length === 0 || !strengths || strengths.length === 0) {
    return [];
  }

  const strengthsMap = new Map();
  strengths.forEach(s => {
    strengthsMap.set(s.team_id, s);
  });

  const maxPosition = Math.max(...strengths.map(s => s.position));
  const bottomCut = maxPosition - 2;

  const results = [];
  
  for (const fixture of fixtures) {
    const home = strengthsMap.get(fixture.home_id);
    const away = strengthsMap.get(fixture.away_id);
    
    if (!home || !away) continue;

    const probs = calculateBTProbabilities(home.rating, away.rating);
    const isTopVsBottom = 
      (home.position <= 4 && away.position >= bottomCut) ||
      (away.position <= 4 && home.position >= bottomCut);

    results.push({
      utcDate: fixture.utcDate,
      matchday: fixture.matchday,
      home: home.team,
      home_pos: home.position,
      away: away.team,
      away_pos: away.position,
      'P(Home)': Math.round(probs.pHome * 1000) / 1000,
      'P(Draw)': Math.round(probs.pDraw * 1000) / 1000,
      'P(Away)': Math.round(probs.pAway * 1000) / 1000,
      ALERTA: isTopVsBottom ? '⚠️ Top-4 × Bottom-3' : ''
    });
  }

  // Ordenar: alertas primeiro, depois por data
  results.sort((a, b) => {
    if (a.ALERTA && !b.ALERTA) return -1;
    if (!a.ALERTA && b.ALERTA) return 1;
    if (a.utcDate !== b.utcDate) return a.utcDate.localeCompare(b.utcDate);
    return (a.matchday || 0) - (b.matchday || 0);
  });

  return results;
}

// Formatar data BR
function formatDateBR(isoString) {
  try {
    const dt = new Date(isoString.replace('Z', '+00:00'));
    const day = String(dt.getUTCDate()).padStart(2, '0');
    const month = String(dt.getUTCMonth() + 1).padStart(2, '0');
    const hours = String(dt.getUTCHours()).padStart(2, '0');
    const minutes = String(dt.getUTCMinutes()).padStart(2, '0');
    return `${day}/${month} ${hours}:${minutes}`;
  } catch (e) {
    return isoString;
  }
}

// API Routes

// Rota principal - servir HTML
app.get('/', (req, res) => {
  res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// API: Obter dados da liga
app.post('/api/league-data', async (req, res) => {
  try {
    const { token, leagueCode, dateFrom, dateTo, daysAhead } = req.body;

    if (!token) {
      return res.status(400).json({ error: 'API token é obrigatório' });
    }

    const standings = await getTotalStanding(token, leagueCode);
    const strengths = calculateLeagueStrengths(standings);
    const fixtures = await getUpcomingMatches(token, leagueCode, dateFrom, dateTo, daysAhead);
    const probabilities = calculateMatchProbabilities(fixtures, strengths);

    res.json({
      standings,
      strengths,
      fixtures,
      probabilities
    });
  } catch (error) {
    console.error('Erro ao buscar dados:', error);
    res.status(500).json({ 
      error: error.message || 'Erro ao buscar dados da API' 
    });
  }
});

// Limpar cache
app.post('/api/clear-cache', (req, res) => {
  cache.clear();
  res.json({ message: 'Cache limpo' });
});

// Listar competições disponíveis
app.post('/api/list-competitions', async (req, res) => {
  try {
    const { token } = req.body;

    if (!token) {
      return res.status(400).json({ error: 'API token é obrigatório' });
    }

    const url = `${API_BASE}/competitions`;
    const data = await requestWithRetry(url, token);

    // Formatar resposta para facilitar visualização
    const competitions = (data.competitions || []).map(comp => ({
      code: comp.code,
      name: comp.name,
      type: comp.type,
      emblem: comp.emblem,
      plan: comp.plan, // Indica se é free, tier-one, etc.
      area: comp.area ? {
        name: comp.area.name,
        code: comp.area.code
      } : null
    }));

    // Ordenar por nome
    competitions.sort((a, b) => a.name.localeCompare(b.name));

    res.json({
      total: competitions.length,
      competitions
    });
  } catch (error) {
    console.error('Erro ao listar competições:', error);
    res.status(500).json({ 
      error: error.message || 'Erro ao listar competições da API' 
    });
  }
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
  console.log(`🚀 Servidor rodando em http://localhost:${PORT}`);
  console.log(`📱 Configure o app Android para: http://localhost:${PORT}`);
});

