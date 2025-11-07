// Adaptador para API FootyStats
// Nota: Este é um template - precisa ser configurado com a API key e endpoints corretos
const axios = require('axios');

class FootyStatsAdapter {
  constructor() {
    this.name = 'footystats';
    this.baseUrl = 'https://api.footystats.org'; // Verificar URL correta na documentação
    // Liga IDs da FootyStats (precisam ser mapeados)
    this.leagueMapping = {
      'RFPL': 123, // Russian Premier League - ID precisa ser verificado
      'UPL': 124,  // Ukrainian Premier League - ID precisa ser verificado
      'SAL': 125,  // Saudi Pro League - ID precisa ser verificado
      'TUR': 126,  // Turkish Süper Lig - ID precisa ser verificado
      'CL1': 127   // Chinese Super League - ID precisa ser verificado
    };
  }

  // Mapear código da liga para o formato da API
  getLeagueCode(leagueCode) {
    return this.leagueMapping[leagueCode] || leagueCode;
  }

  // Verificar se a liga é suportada por esta API
  supportsLeague(leagueCode) {
    return this.leagueMapping.hasOwnProperty(leagueCode) || 
           ['BL1', 'PL', 'FL1', 'DED', 'BSA', 'PD'].includes(leagueCode);
  }

  // Obter standings (classificação)
  async getStandings(token, leagueCode) {
    const apiCode = this.getLeagueCode(leagueCode);
    // Endpoint precisa ser verificado na documentação da FootyStats
    const url = `${this.baseUrl}/standings/${apiCode}`;
    
    try {
      const response = await axios.get(url, {
        headers: token ? { 'Authorization': `Bearer ${token}` } : {}, // Verificar formato correto
        timeout: 30000
      });

      if (response.status >= 400) {
        throw new Error(`HTTP ${response.status}: ${response.data?.message || 'Error'}`);
      }

      // Converter formato da FootyStats para formato padrão
      // Isso precisa ser ajustado baseado na estrutura real da resposta
      const rows = (response.data.data || response.data || []).map((row, index) => ({
        position: row.position || index + 1,
        team_id: row.team_id || row.id,
        team: row.team || row.name,
        tla: row.tla || row.short_name || '',
        played: row.played || row.playedGames || 0,
        won: row.won || 0,
        draw: row.draw || 0,
        lost: row.lost || 0,
        gf: row.goalsFor || row.gf || 0,
        ga: row.goalsAgainst || row.ga || 0,
        gd: row.goalDifference || row.gd || 0,
        points: row.points || 0,
        form: row.form || ''
      }));

      return rows;
    } catch (error) {
      if (error.response) {
        const status = error.response.status;
        throw new Error(`HTTP ${status}: ${error.response.data?.message || error.response.data?.error || 'Error'}`);
      }
      throw error;
    }
  }

  // Obter próximos jogos
  async getUpcomingMatches(token, leagueCode, dateFrom = null, dateTo = null, daysAhead = 10) {
    const apiCode = this.getLeagueCode(leagueCode);
    // Endpoint precisa ser verificado na documentação da FootyStats
    const url = `${this.baseUrl}/fixtures/${apiCode}`;
    
    let fromDate = dateFrom;
    let toDate = dateTo;
    
    if (!fromDate || !toDate) {
      const today = new Date();
      today.setUTCHours(0, 0, 0, 0);
      fromDate = fromDate || today.toISOString().split('T')[0];
      toDate = toDate || new Date(today.getTime() + daysAhead * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
    }

    try {
      const response = await axios.get(url, {
        headers: token ? { 'Authorization': `Bearer ${token}` } : {}, // Verificar formato correto
        params: {
          dateFrom: fromDate,
          dateTo: toDate
        },
        timeout: 30000
      });

      if (response.status >= 400) {
        throw new Error(`HTTP ${response.status}: ${response.data?.message || 'Error'}`);
      }

      // Converter formato da FootyStats para formato padrão
      const rows = (response.data.data || response.data || []).map(match => ({
        match_id: match.id || match.match_id,
        utcDate: match.date || match.utcDate || match.datetime,
        status: match.status || 'SCHEDULED',
        matchday: match.round || match.matchday || null,
        home_id: match.home_team_id || match.homeTeam?.id,
        home: match.home_team || match.homeTeam?.name,
        home_tla: match.home_team_tla || match.homeTeam?.tla || '',
        away_id: match.away_team_id || match.awayTeam?.id,
        away: match.away_team || match.awayTeam?.name,
        away_tla: match.away_team_tla || match.awayTeam?.tla || ''
      }));

      return rows;
    } catch (error) {
      if (error.response) {
        const status = error.response.status;
        throw new Error(`HTTP ${status}: ${error.response.data?.message || error.response.data?.error || 'Error'}`);
      }
      throw error;
    }
  }
}

module.exports = new FootyStatsAdapter();

