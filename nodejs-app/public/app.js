// Configuração
const BASE_LEAGUES = {
    'BL1': 'Alemanha - Bundesliga',
    'PL': 'Inglaterra - Premier League',
    'FL1': 'França - Ligue 1',
    'DED': 'Holanda - Eredivisie',
    'BSA': 'Brasil - Série A',
    'PD': 'Espanha - La Liga',
    'RFPL': 'Rússia - Premier League',
    'UPL': 'Ucrânia - Premier League',
    'SAL': 'Arábia Saudita - Pro League',
    'TUR': 'Turquia - Süper Lig',
    'CL1': 'China - Super League',
    'CL': 'Champions League'
};

// Elementos DOM
const leaguesContainer = document.getElementById('leaguesContainer');
const daysSlider = document.getElementById('days');
const daysValue = document.getElementById('daysValue');
const dateFromInput = document.getElementById('dateFrom');
const dateToInput = document.getElementById('dateTo');
const refreshBtn = document.getElementById('refreshBtn');
const clearCacheBtn = document.getElementById('clearCacheBtn');
const loadingDiv = document.getElementById('loading');
const errorDiv = document.getElementById('error');
const contentDiv = document.getElementById('content');

// Event Listeners
daysSlider.addEventListener('input', (e) => {
    daysValue.textContent = e.target.value;
});

refreshBtn.addEventListener('click', () => {
    loadData();
});

clearCacheBtn.addEventListener('click', async () => {
    try {
        const response = await fetch('/api/clear-cache', { method: 'POST' });
        const data = await response.json();
        alert('Cache limpo com sucesso!');
    } catch (error) {
        console.error('Erro ao limpar cache:', error);
        alert('Erro ao limpar cache');
    }
});

// Carregar dados
async function loadData() {
    const selectedLeagues = Array.from(leaguesContainer.querySelectorAll('input[type="checkbox"]:checked')).map(cb => cb.value);
    
    if (selectedLeagues.length === 0) {
        showError('Selecione ao menos uma liga');
        return;
    }

    // Atualizar lista de ligas baseado no checkbox CL
    updateLeaguesList();

    const days = parseInt(daysSlider.value);
    const dateFrom = dateFromInput.value || null;
    const dateTo = dateToInput.value || null;

    showLoading();
    hideError();
    contentDiv.innerHTML = '';

    for (const leagueCode of selectedLeagues) {
        try {
            await loadLeagueData(leagueCode, dateFrom, dateTo, days);
        } catch (error) {
            console.error(`Erro ao carregar ${leagueCode}:`, error);
            showError(`Erro ao carregar ${BASE_LEAGUES[leagueCode]}: ${error.message}`);
        }
    }

    hideLoading();
}

async function loadLeagueData(leagueCode, dateFrom, dateTo, daysAhead) {
    try {
        const response = await fetch('/api/league-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                leagueCode,
                dateFrom,
                dateTo,
                daysAhead
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Erro ao buscar dados');
        }

        const data = await response.json();
        renderLeagueSection(leagueCode, data);
    } catch (error) {
        throw error;
    }
}

function renderLeagueSection(leagueCode, data) {
    const leagueName = BASE_LEAGUES[leagueCode] || leagueCode;
    const { standings, fixtures, probabilities } = data;

    const section = document.createElement('div');
    section.className = 'league-section';
    section.innerHTML = `<h3>${leagueName} (${leagueCode})</h3>`;

    const columns = document.createElement('div');
    columns.className = 'columns';

    // Coluna 1: Classificação
    const col1 = document.createElement('div');
    col1.className = 'column';
    col1.innerHTML = '<h4>Classificação</h4>';

    if (!standings || standings.length === 0) {
        col1.innerHTML += '<div class="info-message">Sem standings para esta liga.</div>';
    } else {
        const standingsTable = createStandingsTable(standings);
        col1.appendChild(standingsTable);
        
        const downloadBtn = document.createElement('a');
        downloadBtn.href = '#';
        downloadBtn.className = 'download-btn';
        downloadBtn.textContent = '⬇️ Baixar CSV (Classificação)';
        downloadBtn.onclick = (e) => {
            e.preventDefault();
            downloadCSV(standings, `standings_${leagueCode}.csv`);
        };
        col1.appendChild(downloadBtn);
    }

    // Coluna 2: Jogos + Probabilidades
    const col2 = document.createElement('div');
    col2.className = 'column';
    col2.innerHTML = `<h4>Próximos jogos (${daysSlider.value} dias)</h4>`;

    if (!fixtures || fixtures.length === 0) {
        col2.innerHTML += '<div class="info-message">Sem jogos agendados no período.</div>';
    } else if (!probabilities || probabilities.length === 0) {
        const fixturesTable = createFixturesTable(fixtures);
        col2.appendChild(fixturesTable);
        col2.innerHTML += '<div class="info-message">Não foi possível calcular probabilidades (dados insuficientes).</div>';
    } else {
        const probsTable = createProbabilitiesTable(probabilities, standings);
        col2.appendChild(probsTable);
        
        const downloadBtn = document.createElement('a');
        downloadBtn.href = '#';
        downloadBtn.className = 'download-btn';
        downloadBtn.textContent = '⬇️ Baixar CSV (Jogos + Prob.)';
        downloadBtn.onclick = (e) => {
            e.preventDefault();
            downloadCSV(probabilities.map(p => ({
                'Data (BR)': formatDateBR(p.utcDate),
                matchday: p.matchday,
                home: p.home,
                'home_pos': p.home_pos,
                away: p.away,
                'away_pos': p.away_pos,
                'P(Home)%': Math.round(p['P(Home)'] * 100),
                'P(Draw)%': Math.round(p['P(Draw)'] * 100),
                'P(Away)%': Math.round(p['P(Away)'] * 100),
                ALERTA: p.ALERTA
            })), `fixtures_probs_${leagueCode}.csv`);
        };
        col2.appendChild(downloadBtn);
    }

    columns.appendChild(col1);
    columns.appendChild(col2);
    section.appendChild(columns);
    contentDiv.appendChild(section);
}

function getTeamCrestUrl(teamId, tla) {
    // Usar API do football-data.org para obter escudo
    if (teamId) {
        return `https://crests.football-data.org/${teamId}.svg`;
    }
    return null;
}

function createStandingsTable(standings) {
    const table = document.createElement('table');
    const thead = document.createElement('thead');
    const tbody = document.createElement('tbody');

    thead.innerHTML = `
        <tr>
            <th>Pos</th>
            <th>Time</th>
            <th>J</th>
            <th>Pts</th>
            <th>SG</th>
            <th>Form</th>
        </tr>
    `;

    const maxPosition = Math.max(...standings.map(t => t.position));
    const bottomCut = maxPosition - 2;

    standings.forEach(team => {
        const tr = document.createElement('tr');
        
        // Adicionar classes para top-4 e bottom-3
        if (team.position <= 4) {
            tr.classList.add('top3');
        } else if (team.position >= bottomCut) {
            tr.classList.add('bottom3');
        }

        const crestUrl = getTeamCrestUrl(team.team_id, team.tla);
        const crestImg = crestUrl 
            ? `<img src="${crestUrl}" alt="${team.team}" class="team-crest" onerror="this.style.display='none'">`
            : '';

        const positionBadge = team.position <= 4 || team.position >= bottomCut
            ? `<span class="position-badge ${team.position <= 4 ? 'top3' : 'bottom3'}">${team.position}</span>`
            : team.position;

        tr.innerHTML = `
            <td>${positionBadge}</td>
            <td>
                <span class="team-name">
                    ${crestImg}
                    ${team.team}
                </span>
            </td>
            <td>${team.played}</td>
            <td><strong>${team.points}</strong></td>
            <td>${team.gd > 0 ? '+' : ''}${team.gd}</td>
            <td>${formatForm(team.form) || '-'}</td>
        `;
        tbody.appendChild(tr);
    });

    table.appendChild(thead);
    table.appendChild(tbody);
    return table;
}

function formatForm(form) {
    if (!form) return null;
    return form.split('').map(result => {
        switch(result) {
            case 'W': return '<span style="color: #4caf50;">W</span>';
            case 'D': return '<span style="color: #ffc107;">D</span>';
            case 'L': return '<span style="color: #f44336;">L</span>';
            default: return result;
        }
    }).join('');
}

function createFixturesTable(fixtures) {
    const table = document.createElement('table');
    const thead = document.createElement('thead');
    const tbody = document.createElement('tbody');

    thead.innerHTML = `
        <tr>
            <th>Data (BR)</th>
            <th>Rodada</th>
            <th>Casa</th>
            <th>Visitante</th>
        </tr>
    `;

    fixtures.forEach(match => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${formatDateBR(match.utcDate)}</td>
            <td>${match.matchday || '-'}</td>
            <td>${match.home}</td>
            <td>${match.away}</td>
        `;
        tbody.appendChild(tr);
    });

    table.appendChild(thead);
    table.appendChild(tbody);
    return table;
}

function createProbabilitiesTable(probabilities, standings = []) {
    const table = document.createElement('table');
    const thead = document.createElement('thead');
    const tbody = document.createElement('tbody');

    // Criar mapa de times para buscar escudos
    const teamsMap = new Map();
    standings.forEach(team => {
        teamsMap.set(team.team, { id: team.team_id, tla: team.tla });
    });

    thead.innerHTML = `
        <tr>
            <th>Data (BR)</th>
            <th>Rodada</th>
            <th>Casa</th>
            <th>Pos</th>
            <th>vs</th>
            <th>Visitante</th>
            <th>Pos</th>
            <th>P(Casa)%</th>
            <th>P(Empate)%</th>
            <th>P(Visitante)%</th>
            <th>Alerta</th>
        </tr>
    `;

    probabilities.forEach(match => {
        const tr = document.createElement('tr');
        
        // Destacar se for Top-4 vs Bottom-3
        if (match.ALERTA) {
            tr.classList.add('top3');
        }

        const alertCell = match.ALERTA 
            ? `<span class="alert-badge">${match.ALERTA}</span>`
            : '';

        // Buscar escudos
        const homeTeam = teamsMap.get(match.home);
        const awayTeam = teamsMap.get(match.away);
        const homeCrest = homeTeam ? getTeamCrestUrl(homeTeam.id, homeTeam.tla) : null;
        const awayCrest = awayTeam ? getTeamCrestUrl(awayTeam.id, awayTeam.tla) : null;

        const homeCrestImg = homeCrest 
            ? `<img src="${homeCrest}" alt="${match.home}" class="team-crest" onerror="this.style.display='none'">`
            : '';
        const awayCrestImg = awayCrest 
            ? `<img src="${awayCrest}" alt="${match.away}" class="team-crest" onerror="this.style.display='none'">`
            : '';

        const maxPos = standings.length > 0 ? Math.max(...standings.map(s => s.position)) : 0;
        const bottomCut = maxPos - 2;

        const homePosBadge = match.home_pos <= 4 
            ? `<span class="position-badge top3">${match.home_pos}</span>`
            : match.home_pos >= bottomCut && maxPos > 0
            ? `<span class="position-badge bottom3">${match.home_pos}</span>`
            : match.home_pos;

        const awayPosBadge = match.away_pos <= 4 
            ? `<span class="position-badge top3">${match.away_pos}</span>`
            : match.away_pos >= bottomCut && maxPos > 0
            ? `<span class="position-badge bottom3">${match.away_pos}</span>`
            : match.away_pos;

        // Calcular cor da probabilidade (verde para maior, vermelho para menor)
        const homeProb = Math.round(match['P(Home)'] * 100);
        const drawProb = Math.round(match['P(Draw)'] * 100);
        const awayProb = Math.round(match['P(Away)'] * 100);

        const maxProb = Math.max(homeProb, drawProb, awayProb);
        const homeProbColor = homeProb === maxProb ? '#4caf50' : 'inherit';
        const drawProbColor = drawProb === maxProb ? '#ffc107' : 'inherit';
        const awayProbColor = awayProb === maxProb ? '#4caf50' : 'inherit';

        tr.innerHTML = `
            <td>${formatDateBR(match.utcDate)}</td>
            <td>${match.matchday || '-'}</td>
            <td>
                <span class="team-name">
                    ${homeCrestImg}
                    ${match.home}
                </span>
            </td>
            <td>${homePosBadge}</td>
            <td style="text-align: center; font-weight: bold; color: var(--text-secondary);">vs</td>
            <td>
                <span class="team-name">
                    ${awayCrestImg}
                    ${match.away}
                </span>
            </td>
            <td>${awayPosBadge}</td>
            <td style="color: ${homeProbColor}; font-weight: ${homeProb === maxProb ? 'bold' : 'normal'}">${homeProb}%</td>
            <td style="color: ${drawProbColor}; font-weight: ${drawProb === maxProb ? 'bold' : 'normal'}">${drawProb}%</td>
            <td style="color: ${awayProbColor}; font-weight: ${awayProb === maxProb ? 'bold' : 'normal'}">${awayProb}%</td>
            <td>${alertCell}</td>
        `;
        tbody.appendChild(tr);
    });

    table.appendChild(thead);
    table.appendChild(tbody);
    return table;
}

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

function downloadCSV(data, filename) {
    if (!data || data.length === 0) return;

    const headers = Object.keys(data[0]);
    const csv = [
        headers.join(','),
        ...data.map(row => 
            headers.map(header => {
                const value = row[header];
                return typeof value === 'string' && value.includes(',') 
                    ? `"${value}"` 
                    : value;
            }).join(',')
        )
    ].join('\n');

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
}

function updateLeaguesList() {
    const leaguesContainer = document.getElementById('leaguesContainer');
    const clLeagueItem = document.getElementById('clLeagueItem');
    
    if (clLeagueItem) {
        // Desmarcar CL se estiver marcado
        const clCheckbox = clLeagueItem.querySelector('input[type="checkbox"]');
        if (clCheckbox) clCheckbox.checked = false;
    }
}

function showLoading() {
    loadingDiv.classList.remove('hidden');
}

function hideLoading() {
    loadingDiv.classList.add('hidden');
}

function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}

function hideError() {
    errorDiv.classList.add('hidden');
}

// Inicialização - garantir que CL apareça se checkbox estiver marcado
document.addEventListener('DOMContentLoaded', () => {
    updateLeaguesList();
});

