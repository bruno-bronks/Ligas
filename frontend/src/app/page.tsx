"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

interface LeagueSummary {
  code: string;
  name: string;
  country: string;
  flag_emoji: string;
  leader_team: string | null;
  leader_points: number | null;
}

interface OverviewData {
  total_leagues: number;
  total_teams: number;
  total_matches: number;
  total_goals: number;
  leagues: LeagueSummary[];
  upcoming_g3_vs_z3: number;
}

interface MatchHighlight {
  id: number;
  home_team: string;
  away_team: string;
  home_team_logo: string | null;
  away_team_logo: string | null;
  home_score: number | null;
  away_score: number | null;
  status: string;
  match_date: string;
  is_g3_vs_z3: boolean;
}

interface HighlightsData {
  highlighted_matches: MatchHighlight[];
  live_matches: MatchHighlight[];
  recent_results: MatchHighlight[];
}

export default function Dashboard() {
  const [overview, setOverview] = useState<OverviewData | null>(null);
  const [highlights, setHighlights] = useState<HighlightsData | null>(null);
  const [loading, setLoading] = useState(true);
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

  useEffect(() => {
    async function fetchData() {
      try {
        const [overviewRes, highlightsRes] = await Promise.all([
          fetch(`${API_URL}/dashboard/overview`),
          fetch(`${API_URL}/dashboard/highlights`),
        ]);

        if (!overviewRes.ok || !highlightsRes.ok) {
          throw new Error("Failed to fetch dashboard data");
        }

        const overviewData = await overviewRes.json();
        const highlightsData = await highlightsRes.json();

        setOverview(overviewData);
        setHighlights(highlightsData);
      } catch (err: any) {
        setError(err.message || "Falha ao carregar dados do painel. O servidor backend está rodando?");
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [API_URL]);

  if (loading) {
    return (
      <div className="flex flex-1 flex-col items-center justify-center py-20">
        <div className="h-12 w-12 animate-spin rounded-full border-4 border-emerald-500 border-t-transparent"></div>
        <p className="mt-4 text-zinc-500 dark:text-zinc-400 font-medium">Analisando as condições do gramado...</p>
      </div>
    );
  }

  if (error || !overview || overview.total_leagues === 0) {
    return (
      <div className="flex flex-1 flex-col items-center justify-center py-16 text-center">
        <div className="text-6xl mb-4">🏟️</div>
        <h2 className="text-2xl font-bold text-zinc-900 dark:text-zinc-50">O banco de dados precisa de configuração</h2>
        <p className="mt-2 text-zinc-600 dark:text-zinc-400 max-w-md">
          Para começar, por favor certifique-se de que o servidor backend está rodando e popule o banco de dados de ligas a partir do Painel Admin.
        </p>
        <div className="mt-6 flex gap-4">
          <Link
            href="/admin"
            className="rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white px-5 py-2.5 text-sm font-semibold transition-all shadow-md"
          >
            Ir para o Painel Admin
          </Link>
          <button
            onClick={() => {
              setLoading(true);
              setError(null);
              window.location.reload();
            }}
            className="rounded-xl border border-zinc-200 dark:border-zinc-800 hover:bg-zinc-100 dark:hover:bg-zinc-900 px-5 py-2.5 text-sm font-semibold transition-all"
          >
            Tentar Conexão Novamente
          </button>
        </div>
      </div>
    );
  }

  const formatMatchDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString(undefined, {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <div className="space-y-10 animate-fade-in">
      {/* Hero Section */}
      <section className="relative rounded-3xl overflow-hidden bg-gradient-to-br from-zinc-900 via-zinc-800 to-emerald-950 p-8 text-white shadow-2xl md:p-12">
        <div className="absolute right-0 top-0 w-1/3 h-full opacity-10 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-teal-400 via-emerald-600 to-indigo-900 blur-2xl"></div>
        <div className="max-w-xl space-y-4">
          <span className="inline-flex items-center gap-1.5 rounded-full bg-emerald-500/20 px-3 py-1 text-xs font-semibold text-emerald-400 backdrop-blur-sm">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
            Inteligência de Futebol IA
          </span>
          <h1 className="text-4xl font-extrabold tracking-tight md:text-5xl">
            Informações Inteligentes em 14 Ligas
          </h1>
          <p className="text-zinc-300 leading-relaxed text-sm md:text-base">
            Monitore ligas de elite de futebol, preveja resultados com nossos modelos de aprendizado de máquina e obtenha atualizações instantâneas sobre confrontos decisivos (G3 vs Z3).
          </p>
        </div>
      </section>

      {/* Stats Counter */}
      <section className="grid grid-cols-2 gap-4 md:grid-cols-4">
        {[
          { label: "Ligas Monitoradas", value: overview.total_leagues, icon: "🏆", color: "from-blue-500/10 to-indigo-500/5 text-blue-500" },
          { label: "Total de Times", value: overview.total_teams, icon: "🛡️", color: "from-amber-500/10 to-orange-500/5 text-amber-500" },
          { label: "Partidas Sincronizadas", value: overview.total_matches, icon: "⚽", color: "from-emerald-500/10 to-teal-500/5 text-emerald-500" },
          { label: "Gols Registrados", value: overview.total_goals, icon: "🥅", color: "from-rose-500/10 to-pink-500/5 text-rose-500" },
        ].map((stat, idx) => (
          <div key={idx} className="relative overflow-hidden rounded-2xl border border-zinc-200/60 bg-white p-6 shadow-sm dark:border-zinc-800/60 dark:bg-zinc-900/40">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-zinc-500 dark:text-zinc-400">{stat.label}</span>
              <span className="text-2xl">{stat.icon}</span>
            </div>
            <div className="mt-4 flex items-baseline gap-2">
              <span className="text-3xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50">{stat.value}</span>
            </div>
          </div>
        ))}
      </section>

      {/* Live & High-Stakes Grid */}
      <section className="grid gap-6 lg:grid-cols-3">
        {/* Live Matches Panel */}
        <div className="lg:col-span-1 rounded-2xl border border-zinc-200/60 bg-white p-6 shadow-sm dark:border-zinc-800/60 dark:bg-zinc-900/40 flex flex-col h-[400px]">
          <div className="flex items-center justify-between border-b border-zinc-100 dark:border-zinc-800/80 pb-4 mb-4">
            <h3 className="font-bold text-lg flex items-center gap-2">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-rose-500"></span>
              </span>
              Partidas Ao Vivo
            </h3>
            <span className="text-xs bg-rose-100 text-rose-800 dark:bg-rose-950/30 dark:text-rose-400 px-2 py-0.5 rounded-full font-semibold">
              {highlights?.live_matches.length || 0} ativas
            </span>
          </div>

          <div className="flex-1 overflow-y-auto space-y-3 pr-1">
            {!highlights || highlights.live_matches.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-zinc-400 dark:text-zinc-500">
                <span className="text-4xl mb-2">💤</span>
                <p className="text-sm font-medium">Nenhuma partida ao vivo no momento</p>
              </div>
            ) : (
              highlights.live_matches.map((match) => (
                <div key={match.id} className="p-3 rounded-xl border border-rose-500/20 bg-rose-500/5 hover:bg-rose-500/10 transition duration-200">
                  <div className="flex justify-between text-xs text-rose-600 dark:text-rose-400 font-bold mb-1">
                    <span>LIVE</span>
                    <span>{match.status}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="space-y-1 font-semibold text-sm">
                      <div className="flex items-center gap-2">
                        {match.home_team_logo && <img src={getProxiedImageUrl(match.home_team_logo)} className="w-4 h-4 object-contain" alt="" />}
                        <span>{match.home_team}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        {match.away_team_logo && <img src={getProxiedImageUrl(match.away_team_logo)} className="w-4 h-4 object-contain" alt="" />}
                        <span>{match.away_team}</span>
                      </div>
                    </div>
                    <div className="text-right font-mono font-bold text-lg text-rose-600 dark:text-rose-400 bg-rose-500/10 px-2.5 py-1 rounded-lg">
                      {match.home_score} - {match.away_score}
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* G3 vs Z3 Highlights */}
        <div className="lg:col-span-2 rounded-2xl border border-zinc-200/60 bg-white p-6 shadow-sm dark:border-zinc-800/60 dark:bg-zinc-900/40 flex flex-col h-[400px]">
          <div className="flex items-center justify-between border-b border-zinc-100 dark:border-zinc-800/80 pb-4 mb-4">
            <h3 className="font-bold text-lg flex items-center gap-2">
              <span className="text-xl">🔥</span>
              Confrontos Assimétricos (G3 vs Z3)
            </h3>
            <span className="text-xs bg-amber-100 text-amber-800 dark:bg-amber-950/30 dark:text-amber-400 px-2 py-0.5 rounded-full font-semibold">
              {overview.upcoming_g3_vs_z3} próximos
            </span>
          </div>

          <div className="flex-1 overflow-y-auto space-y-3 pr-1">
            {!highlights || highlights.highlighted_matches.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-zinc-400 dark:text-zinc-500">
                <span className="text-4xl mb-2">🛡️</span>
                <p className="text-sm font-medium">Nenhum confronto G3 vs Z3 agendado para breve</p>
              </div>
            ) : (
              highlights.highlighted_matches.map((match) => (
                <Link
                  href={`/matches/${match.id}`}
                  key={match.id}
                  className="flex items-center justify-between p-4 rounded-xl border border-zinc-100 dark:border-zinc-800 bg-zinc-50/50 hover:bg-zinc-100/50 dark:bg-zinc-900/20 dark:hover:bg-zinc-900/50 transition duration-200"
                >
                  <div className="flex items-center gap-4 flex-1">
                    <div className="flex flex-col items-center justify-center bg-amber-500/10 text-amber-600 dark:text-amber-400 font-bold text-xs h-10 w-10 rounded-lg">
                      <span>VS</span>
                    </div>
                    <div>
                      <div className="font-bold text-sm text-zinc-900 dark:text-zinc-50 flex items-center gap-2">
                        <span>{match.home_team}</span>
                        <span className="text-zinc-400 font-normal">vs</span>
                        <span>{match.away_team}</span>
                      </div>
                      <div className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">
                        {formatMatchDate(match.match_date)}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="hidden sm:inline-flex items-center rounded-full bg-emerald-500/10 px-2.5 py-0.5 text-xs font-medium text-emerald-600 dark:text-emerald-400">
                      Prever e Analisar →
                    </span>
                  </div>
                </Link>
              ))
            )}
          </div>
        </div>
      </section>

      {/* Leagues Summary Grid */}
      <section className="space-y-4">
        <h3 className="font-bold text-xl text-zinc-900 dark:text-zinc-50">Ligas Sincronizadas</h3>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {overview.leagues.map((league) => (
            <Link
              href={`/leagues?code=${league.code}`}
              key={league.code}
              className="group p-5 rounded-2xl border border-zinc-200/60 bg-white hover:border-emerald-500/50 dark:border-zinc-800/60 dark:bg-zinc-900/40 dark:hover:border-emerald-500/50 hover:shadow-md transition-all duration-300"
            >
              <div className="flex items-center gap-3">
                <span className="text-3xl bg-zinc-100 dark:bg-zinc-800 p-2 rounded-xl group-hover:scale-110 transition duration-200">
                  {league.flag_emoji || "⚽"}
                </span>
                <div>
                  <h4 className="font-bold text-zinc-900 dark:text-zinc-50">{league.name}</h4>
                  <span className="text-xs text-zinc-500 dark:text-zinc-400">{league.country}</span>
                </div>
              </div>
              <div className="mt-4 border-t border-zinc-100 dark:border-zinc-850 pt-3 flex items-center justify-between text-xs text-zinc-500 dark:text-zinc-400">
                <span>Líder:</span>
                <span className="font-semibold text-zinc-800 dark:text-zinc-350">
                  {league.leader_team ? `${league.leader_team} (${league.leader_points} pts)` : "N/A"}
                </span>
              </div>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
