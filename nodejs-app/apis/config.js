// Configuração das APIs disponíveis
// Ordem de tentativa: primeira API é tentada primeiro, depois fallback para as seguintes

module.exports = {
  apis: [
    {
      name: 'football-data',
      enabled: true,
      priority: 1, // Prioridade mais alta (tentada primeiro)
      adapter: require('./football-data'),
      leagues: {
        'BL1': 'Bundesliga',
        'PL': 'Premier League',
        'FL1': 'Ligue 1',
        'DED': 'Eredivisie',
        'BSA': 'Brasileirão Série A',
        'PD': 'La Liga',
        'CL': 'Champions League',
        'SA': 'Serie A',
        'EL': 'Europa League',
        'EC': 'European Championship',
        'WC': 'World Cup'
      }
    },
    {
      name: 'footystats',
      enabled: false, // Desabilitado por padrão até configurar
      priority: 2,
      adapter: require('./footystats'),
      leagues: {
        'RFPL': 'Russian Premier League',
        'UPL': 'Ukrainian Premier League',
        'SAL': 'Saudi Pro League',
        'TUR': 'Turkish Süper Lig',
        'CL1': 'Chinese Super League',
        // Também pode ter as ligas principais como fallback
        'BL1': 'Bundesliga',
        'PL': 'Premier League',
        'FL1': 'Ligue 1',
        'DED': 'Eredivisie',
        'BSA': 'Brasileirão Série A',
        'PD': 'La Liga'
      }
    }
    // Adicione mais APIs aqui conforme necessário
  ]
};

