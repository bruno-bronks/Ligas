"use client";

import { useState } from "react";

export default function AdminPanel() {
  const [loadingAction, setLoadingAction] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedLeague, setSelectedLeague] = useState("PL");
  const [syncSeason, setSyncSeason] = useState(2024);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

  const leaguesList = [
    { code: "PL", name: "Premier League (England)", flag: "🏴󠁧󠁢󠁥󠁮󠁧󠁿" },
    { code: "BL1", name: "Bundesliga (Germany)", flag: "🇩🇪" },
    { code: "PD", name: "La Liga (Spain)", flag: "🇪🇸" },
    { code: "SA", name: "Serie A (Italy)", flag: "🇮🇹" },
    { code: "FL1", name: "Ligue 1 (France)", flag: "🇫🇷" },
    { code: "DED", name: "Eredivisie (Netherlands)", flag: "🇳🇱" },
    { code: "PPL", name: "Primeira Liga (Portugal)", flag: "🇵🇹" },
    { code: "TSL", name: "Süper Lig (Turkey)", flag: "🇹🇷" },
    { code: "GSL", name: "Super League 1 (Greece)", flag: "🇬🇷" },
    { code: "SAL", name: "Pro League (Saudi Arabia)", flag: "🇸🇦" },
    { code: "QSL", name: "Stars League (Qatar)", flag: "🇶🇦" },
    { code: "MXL", name: "Liga MX (Mexico)", flag: "🇲🇽" },
    { code: "SPL", name: "Premiership (Scotland)", flag: "🏴󠁧󠁢󠁳󠁣󠁴󠁿" },
    { code: "RPL", name: "Premier League (Russia)", flag: "🇷🇺" },
  ];

  const handleAction = async (actionName: string, endpoint: string, method = "POST", body: any = null) => {
    setLoadingAction(actionName);
    setResult(null);
    setError(null);

    try {
      const res = await fetch(`${API_URL}${endpoint}`, {
        method,
        headers: {
          "Content-Type": "application/json",
        },
        body: body ? JSON.stringify(body) : null,
      });

      if (!res.ok) {
        throw new Error(`Action failed with status: ${res.status}`);
      }

      const data = await res.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || "Ocorreu um erro inesperado.");
    } finally {
      setLoadingAction(null);
    }
  };

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      <div>
        <h1 className="text-3xl font-extrabold tracking-tight">Administração do Sistema</h1>
        <p className="text-zinc-500 dark:text-zinc-400 text-sm mt-1">
          Popule o banco de dados, sincronize dados ao vivo de classificação e jogos a partir da API-Football e acione modelos estatísticos/IA.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Core Database Actions */}
        <div className="p-6 rounded-2xl border border-zinc-200/60 bg-white dark:border-zinc-800/60 dark:bg-zinc-900/40 space-y-4">
          <h2 className="text-lg font-bold flex items-center gap-2">
            <span>⚙️</span> Alimentação Principal e Previsão
          </h2>
          <p className="text-xs text-zinc-500">
            Inicialize as ligas e calcule as probabilidades bayesianas para as partidas salvas no banco de dados SQLite local.
          </p>
          
          <div className="flex flex-col gap-3 pt-2">
            {/* Seed Leagues */}
            <button
              onClick={() => handleAction("seed-leagues", "/admin/seed-leagues")}
              disabled={loadingAction !== null}
              className="flex items-center justify-between p-4 rounded-xl border border-zinc-150 dark:border-zinc-800 bg-zinc-50/50 hover:bg-zinc-100 dark:bg-zinc-900/30 hover:border-emerald-500/35 transition duration-200 text-left font-semibold text-sm disabled:opacity-50"
            >
              <div>
                <div className="text-zinc-900 dark:text-zinc-50">1. Popular Ligas Monitoradas</div>
                <div className="text-[11px] text-zinc-400 font-normal mt-0.5">Popula as 14 ligas definidas na configuração.</div>
              </div>
              {loadingAction === "seed-leagues" ? (
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-emerald-500 border-t-transparent"></div>
              ) : (
                <span className="text-emerald-500">Popular →</span>
              )}
            </button>

            {/* Run Predictions */}
            <button
              onClick={() => handleAction("compute-predictions", "/admin/compute-predictions")}
              disabled={loadingAction !== null}
              className="flex items-center justify-between p-4 rounded-xl border border-zinc-150 dark:border-zinc-800 bg-zinc-50/50 hover:bg-zinc-100 dark:bg-zinc-900/30 hover:border-emerald-500/35 transition duration-200 text-left font-semibold text-sm disabled:opacity-50"
            >
              <div>
                <div className="text-zinc-900 dark:text-zinc-50">2. Gerar Previsões de Partidas</div>
                <div className="text-[11px] text-zinc-400 font-normal mt-0.5">Executa o modelo bayesiano em todos os jogos sem previsão.</div>
              </div>
              {loadingAction === "compute-predictions" ? (
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-emerald-500 border-t-transparent"></div>
              ) : (
                <span className="text-emerald-500">Executar →</span>
              )}
            </button>

            {/* Send Digests */}
            <button
              onClick={() => handleAction("send-digest", "/admin/send-digest")}
              disabled={loadingAction !== null}
              className="flex items-center justify-between p-4 rounded-xl border border-zinc-150 dark:border-zinc-800 bg-zinc-50/50 hover:bg-zinc-100 dark:bg-zinc-900/30 hover:border-emerald-500/35 transition duration-200 text-left font-semibold text-sm disabled:opacity-50"
            >
              <div>
                <div className="text-zinc-900 dark:text-zinc-50">3. Disparar Resumo Semanal</div>
                <div className="text-[11px] text-zinc-400 font-normal mt-0.5">Envia notificações (Telegram/WhatsApp) para os próximos jogos.</div>
              </div>
              {loadingAction === "send-digest" ? (
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-emerald-500 border-t-transparent"></div>
              ) : (
                <span className="text-emerald-500">Enviar →</span>
              )}
            </button>
          </div>
        </div>

        {/* Sync Leagues Panel */}
        <div className="p-6 rounded-2xl border border-zinc-200/60 bg-white dark:border-zinc-800/60 dark:bg-zinc-900/40 space-y-4">
          <h2 className="text-lg font-bold flex items-center gap-2">
            <span>📡</span> Sincronização de Dados Ao Vivo
          </h2>
          <p className="text-xs text-zinc-500">
            Busque times, classificações e jogos ao vivo do serviço API-Football. Isso atualiza o banco de dados SQLite local.
          </p>

          <div className="space-y-4 pt-2">
            {/* League Dropdown */}
            <div className="flex flex-col gap-1.5">
              <label htmlFor="admin-league" className="text-xs font-semibold text-zinc-500">Liga Alvo:</label>
              <select
                id="admin-league"
                value={selectedLeague}
                onChange={(e) => setSelectedLeague(e.target.value)}
                className="w-full rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 px-3.5 py-2.5 text-sm font-semibold shadow-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
              >
                {leaguesList.map((l) => (
                  <option key={l.code} value={l.code}>
                    {l.flag} {l.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Season Input */}
            <div className="flex flex-col gap-1.5">
              <label htmlFor="admin-season" className="text-xs font-semibold text-zinc-500">Ano da Temporada:</label>
              <input
                id="admin-season"
                type="number"
                value={syncSeason}
                onChange={(e) => setSyncSeason(parseInt(e.target.value) || 2024)}
                className="w-full rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 px-3.5 py-2.5 text-sm font-semibold shadow-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            <button
              onClick={() => handleAction(`sync-${selectedLeague}`, `/admin/sync/${selectedLeague}?season=${syncSeason}`)}
              disabled={loadingAction !== null}
              className="w-full mt-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-sm py-3 transition duration-200 flex items-center justify-center gap-2 shadow-md disabled:opacity-50"
            >
              {loadingAction === `sync-${selectedLeague}` ? (
                <>
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></div>
                  <span>Sincronizando Dados Ao Vivo...</span>
                </>
              ) : (
                <span>Sincronizar Liga Selecionada</span>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Execution Results */}
      {(result || error) && (
        <div className="p-6 rounded-2xl border border-zinc-200/60 bg-white dark:border-zinc-800/60 dark:bg-zinc-900/40 space-y-3">
          <div className="flex items-center justify-between border-b border-zinc-100 dark:border-zinc-800/80 pb-3">
            <h3 className="font-bold text-sm">Resultado da Execução</h3>
            <button
              onClick={() => {
                setResult(null);
                setError(null);
              }}
              className="text-xs text-zinc-400 hover:text-zinc-500"
            >
              Limpar
            </button>
          </div>
          {error ? (
            <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-500 text-sm font-medium">
              ❌ {error}
            </div>
          ) : (
            <pre className="p-4 rounded-xl bg-zinc-50 dark:bg-zinc-950 font-mono text-xs overflow-x-auto text-zinc-700 dark:text-zinc-300 max-h-[300px]">
              {JSON.stringify(result, null, 2)}
            </pre>
          )}
        </div>
      )}
    </div>
  );
}
