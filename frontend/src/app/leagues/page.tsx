"use client";

import { useEffect, useState, use } from "react";
import Link from "next/link";
import { useSearchParams, useRouter } from "next/navigation";

interface LeagueResponse {
  code: string;
  name: string;
  country: string;
  flag_emoji: string;
}

interface StandingRow {
  position: number;
  team_id: number;
  team_name: string;
  team_logo: string | null;
  played: number;
  won: number;
  drawn: number;
  lost: number;
  goals_for: number;
  goals_against: number;
  goal_difference: number;
  points: number;
  form: string | null;
  description: string | null;
}

interface StandingsTable {
  league_code: string;
  league_name: string;
  season_year: string;
  standings: StandingRow[];
  g3_teams: number[];
  z3_teams: number[];
}

interface MatchFixture {
  id: number;
  home_team: string;
  away_team: string;
  home_team_logo: string | null;
  away_team_logo: string | null;
  match_date: string;
  matchday: number | null;
  venue: string | null;
  is_g3_vs_z3: boolean;
  home_score?: number | null;
  away_score?: number | null;
}

export default function LeaguesExplorer() {
  const searchParams = useSearchParams();
  const router = useRouter();
  
  // State variables
  const [leagues, setLeagues] = useState<LeagueResponse[]>([]);
  const [selectedLeagueCode, setSelectedLeagueCode] = useState<string>("");
  const [standings, setStandings] = useState<StandingsTable | null>(null);
  const [fixtures, setFixtures] = useState<MatchFixture[]>([]);
  const [results, setResults] = useState<MatchFixture[]>([]);
  const [activeTab, setActiveTab] = useState<"standings" | "fixtures" | "results">("standings");
  const [loading, setLoading] = useState(true);
  const [detailsLoading, setDetailsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const getApiUrl = (): string => {
    if (typeof window !== "undefined") {
      const host = window.location.hostname;
      const port = host === "localhost" || host === "127.0.0.1" ? "8000" : "8001";
      return `http://${host}:${port}/api/v1`;
    }
    return "http://localhost:8000/api/v1";
  };
  const API_URL = getApiUrl();

  const getProxiedImageUrl = (url: string | null): string => {
    if (!url) return "";
    if (url.includes("media.api-sports.io") || url.includes("api-sports.io")) {
      return `${API_URL}/teams/logo-proxy?url=${encodeURIComponent(url)}`;
    }
    return url;
  };

  // Initial fetch of leagues
  useEffect(() => {
    async function fetchLeagues() {
      try {
        const res = await fetch(`${API_URL}/leagues`);
        if (!res.ok) throw new Error("Failed to load leagues");
        const data = await res.json();
        setLeagues(data.leagues || []);
        
        // Select league from URL search param or default to first league
        const codeParam = searchParams.get("code");
        if (codeParam) {
          setSelectedLeagueCode(codeParam.toUpperCase());
        } else if (data.leagues && data.leagues.length > 0) {
          setSelectedLeagueCode(data.leagues[0].code);
        }
      } catch (err: any) {
        setError(err.message || "Falha ao carregar as ligas.");
      } finally {
        setLoading(false);
      }
    }
    fetchLeagues();
  }, [API_URL, searchParams]);

  // Fetch details for selected league
  useEffect(() => {
    if (!selectedLeagueCode) return;

    async function fetchLeagueDetails() {
      setDetailsLoading(true);
      try {
        const [standingsRes, fixturesRes, resultsRes] = await Promise.all([
          fetch(`${API_URL}/leagues/${selectedLeagueCode}/standings`),
          fetch(`${API_URL}/leagues/${selectedLeagueCode}/fixtures`),
          fetch(`${API_URL}/leagues/${selectedLeagueCode}/results`),
        ]);

        if (!standingsRes.ok || !fixturesRes.ok || !resultsRes.ok) {
          throw new Error("Failed to load league details");
        }

        const standingsData = await standingsRes.json();
        const fixturesData = await fixturesRes.json();
        const resultsData = await resultsRes.json();

        setStandings(standingsData);
        setFixtures(fixturesData.fixtures || []);
        setResults(resultsData.results || []);
      } catch (err: any) {
        console.error("Error loading league data:", err);
      } finally {
        setDetailsLoading(false);
      }
    }

    fetchLeagueDetails();
  }, [API_URL, selectedLeagueCode]);

  const handleSelectLeague = (code: string) => {
    setSelectedLeagueCode(code);
    router.push(`/leagues?code=${code}`);
  };

  const formatMatchDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString(undefined, {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  if (loading) {
    return (
      <div className="flex flex-1 flex-col items-center justify-center py-20">
        <div className="h-12 w-12 animate-spin rounded-full border-4 border-emerald-500 border-t-transparent"></div>
        <p className="mt-4 text-zinc-500 dark:text-zinc-400 font-medium">Carregando Ligas...</p>
      </div>
    );
  }

  if (error || leagues.length === 0) {
    return (
      <div className="text-center py-16">
        <div className="text-5xl mb-4">🏆</div>
        <h3 className="text-xl font-bold">Nenhuma Liga Encontrada</h3>
        <p className="text-zinc-500 mt-2">Certifique-se de popular as ligas no Painel Admin.</p>
        <Link href="/admin" className="mt-4 inline-block bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2 rounded-xl text-sm font-semibold transition-all">
          Ir para o Painel Admin
        </Link>
      </div>
    );
  }

  const selectedLeague = leagues.find((l) => l.code === selectedLeagueCode);

  return (
    <div className="space-y-6">
      {/* Selector and Header */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight flex items-center gap-2">
            <span>{selectedLeague?.flag_emoji || "🏆"}</span>
            <span>{selectedLeague?.name || "Detalhes da Liga"}</span>
          </h1>
          <p className="text-zinc-500 dark:text-zinc-400 text-sm">
            {selectedLeague?.country} • Temporada {standings?.season_year || "2024"}
          </p>
        </div>

        {/* Dropdown Selector */}
        <div className="flex items-center gap-2">
          <label htmlFor="league-select" className="text-sm font-medium text-zinc-500">Selecionar Liga:</label>
          <select
            id="league-select"
            value={selectedLeagueCode}
            onChange={(e) => handleSelectLeague(e.target.value)}
            className="rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 px-4 py-2.5 text-sm font-semibold shadow-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
          >
            {leagues.map((l) => (
              <option key={l.code} value={l.code}>
                {l.flag_emoji} {l.name} ({l.country})
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-zinc-250 dark:border-zinc-800">
        <div className="flex gap-2">
          {[
            { id: "standings", label: "Tabela de Classificação", icon: "📊" },
            { id: "fixtures", label: "Próximos Jogos", icon: "📅" },
            { id: "results", label: "Resultados Recentes", icon: "⚽" },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-4 py-3 text-sm font-semibold border-b-2 transition-all duration-200 ${
                activeTab === tab.id
                  ? "border-emerald-500 text-emerald-600 dark:text-emerald-400"
                  : "border-transparent text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100"
              }`}
            >
              <span>{tab.icon}</span>
              <span>{tab.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Content Panels */}
      <div className="min-h-[400px]">
        {detailsLoading ? (
          <div className="flex items-center justify-center py-20">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-emerald-500 border-t-transparent"></div>
          </div>
        ) : activeTab === "standings" ? (
          /* Standings View */
          <div className="overflow-x-auto rounded-2xl border border-zinc-200/60 bg-white shadow-sm dark:border-zinc-800/60 dark:bg-zinc-900/40">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-zinc-200/65 dark:border-zinc-800 bg-zinc-50/50 dark:bg-zinc-900/30 text-xs font-semibold text-zinc-500 uppercase tracking-wider">
                  <th className="py-4 px-4 w-12 text-center">Pos</th>
                  <th className="py-4 px-4">Time</th>
                  <th className="py-4 px-3 text-center">J</th>
                  <th className="py-4 px-3 text-center">V</th>
                  <th className="py-4 px-3 text-center">E</th>
                  <th className="py-4 px-3 text-center">D</th>
                  <th className="py-4 px-3 text-center">GP:GC</th>
                  <th className="py-4 px-3 text-center">SG</th>
                  <th className="py-4 px-3 text-center font-bold">Pts</th>
                  <th className="py-4 px-4 hidden md:table-cell">Forma</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-100 dark:divide-zinc-800/80 text-sm">
                {!standings || standings.standings.length === 0 ? (
                  <tr>
                    <td colSpan={10} className="py-10 text-center text-zinc-400">
                      Nenhum dado de classificação disponível. Certifique-se de sincronizar esta liga no Painel Admin.
                    </td>
                  </tr>
                ) : (
                  standings.standings.map((row) => {
                    const isG3 = standings.g3_teams.includes(row.team_id);
                    const isZ3 = standings.z3_teams.includes(row.team_id);
                    
                    let bgClass = "";
                    if (isG3) bgClass = "bg-emerald-500/5 hover:bg-emerald-500/10 dark:bg-emerald-500/[0.02] dark:hover:bg-emerald-500/5";
                    else if (isZ3) bgClass = "bg-rose-500/5 hover:bg-rose-500/10 dark:bg-rose-500/[0.02] dark:hover:bg-rose-500/5";
                    else bgClass = "hover:bg-zinc-50 dark:hover:bg-zinc-900/30";

                    return (
                      <tr key={row.team_id} className={`transition duration-150 ${bgClass}`}>
                        <td className="py-3.5 px-4 font-bold text-center">
                          <span className={`inline-flex items-center justify-center h-6 w-6 rounded-full text-xs ${
                            isG3 ? "bg-emerald-500 text-white font-extrabold" :
                            isZ3 ? "bg-rose-500 text-white font-extrabold" : "text-zinc-500"
                          }`}>
                            {row.position}
                          </span>
                        </td>
                        <td className="py-3.5 px-4 font-semibold text-zinc-900 dark:text-zinc-50">
                          <div className="flex items-center gap-3">
                            {row.team_logo && (
                              <img src={getProxiedImageUrl(row.team_logo)} className="w-6 h-6 object-contain" alt="" />
                            )}
                            <span>{row.team_name}</span>
                          </div>
                        </td>
                        <td className="py-3.5 px-3 text-center text-zinc-500">{row.played}</td>
                        <td className="py-3.5 px-3 text-center text-emerald-600 dark:text-emerald-400">{row.won}</td>
                        <td className="py-3.5 px-3 text-center text-zinc-500">{row.drawn}</td>
                        <td className="py-3.5 px-3 text-center text-rose-500">{row.lost}</td>
                        <td className="py-3.5 px-3 text-center text-zinc-500 font-mono text-xs">{row.goals_for}:{row.goals_against}</td>
                        <td className={`py-3.5 px-3 text-center font-semibold font-mono text-xs ${
                          row.goal_difference > 0 ? "text-emerald-600 dark:text-emerald-400" :
                          row.goal_difference < 0 ? "text-rose-500" : "text-zinc-500"
                        }`}>
                          {row.goal_difference > 0 ? `+${row.goal_difference}` : row.goal_difference}
                        </td>
                        <td className="py-3.5 px-3 text-center font-bold text-base text-zinc-900 dark:text-zinc-50">{row.points}</td>
                        <td className="py-3.5 px-4 hidden md:table-cell">
                          <div className="flex gap-1.5 justify-start">
                            {row.form?.split("").map((f, i) => {
                              let fColor = "bg-zinc-350 text-white dark:bg-zinc-700";
                              let fLabel = f;
                              if (f === "W") { fColor = "bg-emerald-500 text-white"; fLabel = "V"; }
                              if (f === "L") { fColor = "bg-rose-500 text-white"; fLabel = "D"; }
                              if (f === "D") { fColor = "bg-amber-500 text-white"; fLabel = "E"; }
                              return (
                                <span key={i} className={`inline-flex items-center justify-center text-[10px] font-bold h-5 w-5 rounded-full ${fColor}`}>
                                  {fLabel}
                                </span>
                              );
                            })}
                          </div>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        ) : activeTab === "fixtures" ? (
          /* Fixtures View */
          <div className="grid gap-4 md:grid-cols-2">
            {fixtures.length === 0 ? (
              <div className="md:col-span-2 text-center py-10 border border-zinc-200/60 dark:border-zinc-800 rounded-2xl text-zinc-400 bg-white dark:bg-zinc-900/20">
                Nenhum jogo futuro disponível.
              </div>
            ) : (
              fixtures.map((fixture) => (
                <div
                  key={fixture.id}
                  className={`p-5 rounded-2xl border bg-white dark:bg-zinc-900/30 flex flex-col justify-between shadow-sm relative overflow-hidden transition duration-200 ${
                    fixture.is_g3_vs_z3
                      ? "border-amber-500/40 bg-amber-500/[0.01]"
                      : "border-zinc-200/60 dark:border-zinc-800"
                  }`}
                >
                  {fixture.is_g3_vs_z3 && (
                    <div className="absolute right-0 top-0 bg-gradient-to-l from-amber-500 to-orange-500 text-white px-3 py-1 text-[10px] font-black uppercase tracking-wider rounded-bl-xl shadow-sm">
                      Jogo Assimétrico (G3 vs Z3)
                    </div>
                  )}
                  
                  <div className="space-y-4">
                    <div className="text-xs text-zinc-400 flex items-center justify-between">
                      <span>Rodada {fixture.matchday || "N/A"}</span>
                      <span>{formatMatchDate(fixture.match_date)}</span>
                        <div className="flex items-center justify-between py-2">
                      <div className="flex items-center gap-3 w-[45%]">
                        {fixture.home_team_logo && (
                          <img src={getProxiedImageUrl(fixture.home_team_logo)} className="w-8 h-8 object-contain" alt="" />
                        )}
                        <span className="font-bold text-sm text-zinc-900 dark:text-zinc-50 truncate">{fixture.home_team}</span>
                      </div>
                      <span className="text-xs font-bold text-zinc-400 dark:text-zinc-505 px-2 py-1 bg-zinc-100 dark:bg-zinc-800 rounded-lg">VS</span>
                      <div className="flex items-center gap-3 w-[45%] justify-end text-right">
                        <span className="font-bold text-sm text-zinc-900 dark:text-zinc-50 truncate">{fixture.away_team}</span>
                        {fixture.away_team_logo && (
                          <img src={getProxiedImageUrl(fixture.away_team_logo)} className="w-8 h-8 object-contain" alt="" />
                        )}
                      </div>
                    </div>                  </div>
                  </div>

                  <div className="mt-4 pt-3 border-t border-zinc-100 dark:border-zinc-800/80 flex justify-between items-center text-xs text-zinc-400">
                    <span className="truncate max-w-[200px]">{fixture.venue || "Sem Estádio"}</span>
                    <Link
                      href={`/matches/${fixture.id}`}
                      className="text-emerald-500 dark:text-emerald-400 font-bold hover:underline flex items-center gap-1"
                    >
                      Previsão IA e Análise →
                    </Link>
                  </div>
                </div>
              ))
            )}
          </div>
        ) : (
          /* Results View */
          <div className="grid gap-4 md:grid-cols-2">
            {results.length === 0 ? (
              <div className="md:col-span-2 text-center py-10 border border-zinc-200/60 dark:border-zinc-800 rounded-2xl text-zinc-400 bg-white dark:bg-zinc-900/20">
                Nenhum resultado recente disponível.
              </div>
            ) : (
              results.map((result) => (
                <div
                  key={result.id}
                  className={`p-5 rounded-2xl border bg-white dark:bg-zinc-900/30 flex flex-col justify-between shadow-sm relative overflow-hidden transition duration-200 ${
                    result.is_g3_vs_z3
                      ? "border-amber-500/40 bg-amber-500/[0.01]"
                      : "border-zinc-200/60 dark:border-zinc-800"
                  }`}
                >
                  <div className="space-y-4">
                    <div className="text-xs text-zinc-400 flex items-center justify-between">
                      <span>Rodada {result.matchday || "N/A"}</span>
                      <span>{formatMatchDate(result.match_date)}</span>
                    </div>

                    <div className="flex items-center justify-between py-2">
                      {/* Home */}
                      <div className="flex items-center gap-3 w-[40%]">
                        {result.home_team_logo && (
                          <img src={getProxiedImageUrl(result.home_team_logo)} className="w-8 h-8 object-contain" alt="" />
                        )}
                        <span className="font-bold text-sm text-zinc-900 dark:text-zinc-50 truncate">{result.home_team}</span>
                      </div>
                      
                      {/* Score */}
                      <div className="flex items-center gap-1 text-base font-extrabold font-mono text-zinc-900 dark:text-zinc-50 bg-zinc-150 dark:bg-zinc-800 px-3 py-1.5 rounded-xl shadow-sm">
                        <span>{result.home_score}</span>
                        <span className="text-zinc-400">-</span>
                        <span>{result.away_score}</span>
                      </div>

                      {/* Away */}
                      <div className="flex items-center gap-3 w-[40%] justify-end text-right">
                        <span className="font-bold text-sm text-zinc-900 dark:text-zinc-50 truncate">{result.away_team}</span>
                        {result.away_team_logo && (
                          <img src={getProxiedImageUrl(result.away_team_logo)} className="w-8 h-8 object-contain" alt="" />
                        )}
                      </div>
                    </div>
                  </div>

                  <div className="mt-4 pt-3 border-t border-zinc-100 dark:border-zinc-800/80 flex justify-between items-center text-xs text-zinc-400">
                    <span className="truncate max-w-[200px]">{result.venue || "Sem Estádio"}</span>
                    <Link
                      href={`/matches/${result.id}`}
                      className="text-emerald-500 dark:text-emerald-400 font-bold hover:underline flex items-center gap-1"
                    >
                      Resumo IA e Estatísticas →
                    </Link>
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
}
