// Adaptador para API football-data.org
const axios = require('axios');

class FootballDataAdapter {
  constructor() {
    this.name = 'football-data';
    this.baseUrl = 'https://api.football-data.org/v4';
  }

  // Mapear código da liga para o formato da API
  getLeagueCode(leagueCode) {
    // Retorna o código como está, pois football-data usa os mesmos códigos
    return leagueCode;
  }

  // Verificar se a liga é suportada por esta API
  supportsLeague(leagueCode) {
    const supportedLeagues = ['BL1', 'PL', 'FL1', 'DED', 'BSA', 'PD', 'CL', 'SA', 'EL', 'EC', 'WC'];
    return supportedLeagues.includes(leagueCode);
  }

  // Obter standings (classificação)
  async getStandings(token, leagueCode) {
    const apiCode = this.getLeagueCode(leagueCode);
    const url = `${this.baseUrl}/competitions/${apiCode}/standings`;
    
    try {
      const response = await axios.get(url, {
        headers: token ? { 'X-Auth-Token': token } : {},
        timeout: 30000
      });

      if (response.status >= 400) {
        throw new Error(`HTTP ${response.status}: ${response.data?.message || 'Error'}`);
      }

      const standings = response.data.standings || [];
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
    } catch (error) {
      if (error.response) {
        const status = error.response.status;
        const contentType = error.response.headers['content-type'] || '';
        if (contentType.includes('text/html')) {
          throw new Error(`HTTP ${status}: A API retornou uma página de erro HTML. Verifique sua API key e o endpoint.`);
        }
        throw new Error(`HTTP ${status}: ${error.response.data?.message || error.response.data?.error || 'Error'}`);
      }
      throw error;
    }
  }

  // Obter próximos jogos
  async getUpcomingMatches(token, leagueCode, dateFrom = null, dateTo = null, daysAhead = 10) {
    const apiCode = this.getLeagueCode(leagueCode);
    const url = `${this.baseUrl}/competitions/${apiCode}/matches`;
    
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
        headers: token ? { 'X-Auth-Token': token } : {},
        params: {
          status: 'SCHEDULED,TIMED',
          dateFrom: fromDate,
          dateTo: toDate
        },
        timeout: 30000
      });

      if (response.status >= 400) {
        throw new Error(`HTTP ${response.status}: ${response.data?.message || 'Error'}`);
      }

      const rows = [];
      for (const match of response.data.matches || []) {
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
          away_tla: away.tla
        });
      }

      return rows;
    } catch (error) {
      if (error.response) {
        const status = error.response.status;
        const contentType = error.response.headers['content-type'] || '';
        if (contentType.includes('text/html')) {
          throw new Error(`HTTP ${status}: A API retornou uma página de erro HTML. Verifique sua API key e o endpoint.`);
        }
        throw new Error(`HTTP ${status}: ${error.response.data?.message || error.response.data?.error || 'Error'}`);
      }
      throw error;
    }
  }
}

module.exports = new FootballDataAdapter();

