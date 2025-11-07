// Gerenciador de múltiplas APIs com fallback automático
const config = require('./config');

class APIManager {
  constructor() {
    this.apis = config.apis
      .filter(api => api.enabled)
      .sort((a, b) => a.priority - b.priority);
  }

  // Encontrar APIs que suportam uma liga específica
  findAPIsForLeague(leagueCode) {
    return this.apis.filter(api => {
      return api.leagues.hasOwnProperty(leagueCode) || 
             api.adapter.supportsLeague(leagueCode);
    });
  }

  // Obter standings com fallback automático
  async getStandings(token, leagueCode, apiName = null) {
    let apisToTry = [];
    
    if (apiName) {
      // Tentar API específica primeiro
      const api = this.apis.find(a => a.name === apiName);
      if (api) {
        apisToTry = [api];
      }
    } else {
      // Encontrar APIs que suportam esta liga
      apisToTry = this.findAPIsForLeague(leagueCode);
      
      // Se nenhuma API específica encontrada, tentar todas em ordem de prioridade
      if (apisToTry.length === 0) {
        apisToTry = this.apis;
      }
    }

    const errors = [];
    
    for (const apiConfig of apisToTry) {
      try {
        console.log(`[APIManager] Tentando obter standings de ${leagueCode} via ${apiConfig.name}...`);
        const result = await apiConfig.adapter.getStandings(token, leagueCode);
        console.log(`[APIManager] Sucesso ao obter standings via ${apiConfig.name}`);
        return {
          data: result,
          source: apiConfig.name
        };
      } catch (error) {
        console.error(`[APIManager] Erro ao obter standings via ${apiConfig.name}:`, error.message);
        errors.push({
          api: apiConfig.name,
          error: error.message
        });
        // Continuar para próxima API
        continue;
      }
    }

    // Se todas as APIs falharam, lançar erro
    throw new Error(`Todas as APIs falharam para obter standings de ${leagueCode}. Erros: ${errors.map(e => `${e.api}: ${e.error}`).join('; ')}`);
  }

  // Obter próximos jogos com fallback automático
  async getUpcomingMatches(token, leagueCode, dateFrom = null, dateTo = null, daysAhead = 10, apiName = null) {
    let apisToTry = [];
    
    if (apiName) {
      // Tentar API específica primeiro
      const api = this.apis.find(a => a.name === apiName);
      if (api) {
        apisToTry = [api];
      }
    } else {
      // Encontrar APIs que suportam esta liga
      apisToTry = this.findAPIsForLeague(leagueCode);
      
      // Se nenhuma API específica encontrada, tentar todas em ordem de prioridade
      if (apisToTry.length === 0) {
        apisToTry = this.apis;
      }
    }

    const errors = [];
    
    for (const apiConfig of apisToTry) {
      try {
        console.log(`[APIManager] Tentando obter jogos de ${leagueCode} via ${apiConfig.name}...`);
        const result = await apiConfig.adapter.getUpcomingMatches(token, leagueCode, dateFrom, dateTo, daysAhead);
        console.log(`[APIManager] Sucesso ao obter jogos via ${apiConfig.name}`);
        return {
          data: result,
          source: apiConfig.name
        };
      } catch (error) {
        console.error(`[APIManager] Erro ao obter jogos via ${apiConfig.name}:`, error.message);
        errors.push({
          api: apiConfig.name,
          error: error.message
        });
        // Continuar para próxima API
        continue;
      }
    }

    // Se todas as APIs falharam, lançar erro
    throw new Error(`Todas as APIs falharam para obter jogos de ${leagueCode}. Erros: ${errors.map(e => `${e.api}: ${e.error}`).join('; ')}`);
  }

  // Listar todas as ligas disponíveis em todas as APIs
  getAllAvailableLeagues() {
    const leaguesMap = new Map();
    
    this.apis.forEach(api => {
      Object.keys(api.leagues).forEach(leagueCode => {
        if (!leaguesMap.has(leagueCode)) {
          leaguesMap.set(leagueCode, {
            code: leagueCode,
            name: api.leagues[leagueCode],
            apis: []
          });
        }
        leaguesMap.get(leagueCode).apis.push(api.name);
      });
    });

    return Array.from(leaguesMap.values());
  }
}

module.exports = new APIManager();

