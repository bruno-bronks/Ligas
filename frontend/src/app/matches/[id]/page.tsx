"use client";

import { useEffect, useState, use } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";

interface Prediction {
  home_win_prob: number;
  draw_prob: number;
  away_win_prob: number;
  over_2_5_prob: number | null;
  btts_prob: number | null;
  predicted_outcome: string | null;
}

interface AIAnalysis {
  text: string;
  provider: string;
  model: string;
}

interface MatchDetail {
  id: number;
  home_team: string;
  away_team: string;
  home_team_logo: string | null;
  away_team_logo: string | null;
  home_score: number | null;
  away_score: number | null;
  home_ht_score: number | null;
  away_ht_score: number | null;
  home_xg: number | null;
  away_xg: number | null;
  status: string;
  match_date: string;
  matchday: number | null;
  venue: string | null;
  referee: string | null;
  is_g3_vs_z3: boolean;
  prediction?: Prediction;
  ai_analysis?: AIAnalysis;
}

export default function MatchCenter() {
  const params = useParams();
  const matchId = params?.id;

  const [match, setMatch] = useState<MatchDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [analyzing, setAnalyzing] = useState(false);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

  const getProxiedImageUrl = (url: string | null): string => {
    if (!url) return "";
    if (url.includes("media.api-sports.io") || url.includes("api-sports.io")) {
      return `${API_URL}/teams/logo-proxy?url=${encodeURIComponent(url)}`;
    }
    return url;
  };

  useEffect(() => {
    if (!matchId) return;

    async function fetchMatchDetail() {
      try {
        const res = await fetch(`${API_URL}/matches/${matchId}`);
        if (!res.ok) {
          throw new Error("Falha ao buscar detalhes do jogo");
        }
        const data = await res.json();
        setMatch(data);
      } catch (err: any) {
        setError(err.message || "Falha ao carregar detalhes do jogo.");
      } finally {
        setLoading(false);
      }
    }

    fetchMatchDetail();
  }, [API_URL, matchId]);

  const handleGenerateAnalysis = async () => {
    if (!matchId) return;
    setAnalyzing(true);
    try {
      const res = await fetch(`${API_URL}/matches/${matchId}/analyze`, {
        method: "POST",
      });
      if (!res.ok) throw new Error("Falha ao gerar análise de IA");
      const data = await res.json();
      
      setMatch(prev => prev ? {
        ...prev,
        ai_analysis: {
          text: data.text,
          provider: data.provider,
          model: data.model
        }
      } : null);
    } catch (err: any) {
      alert(err.message || "Falha ao gerar análise.");
    } finally {
      setAnalyzing(false);
    }
  };

  const formatMatchDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("pt-BR", {
      weekday: "long",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const renderMarkdown = (text: string) => {
    const sections = text.split("###");
    return sections.map((section, idx) => {
      if (!section.trim()) return null;
      const lines = section.split("\n");
      const title = lines[0].trim();
      const content = lines.slice(1).join("\n").trim();
      
      return (
        <div key={idx} className="space-y-3 mb-6 last:mb-0">
          {title && (
            <h4 className="text-base font-bold text-zinc-900 dark:text-zinc-50 border-b border-zinc-150 dark:border-zinc-800 pb-2 flex items-center gap-2">
              <span>{title}</span>
            </h4>
          )}
          <div className="text-sm leading-relaxed text-zinc-600 dark:text-zinc-400 whitespace-pre-line">
            {content}
          </div>
        </div>
      );
    });
  };

  if (loading) {
    return (
      <div className="flex flex-1 flex-col items-center justify-center py-20">
        <div className="h-12 w-12 animate-spin rounded-full border-4 border-emerald-500 border-t-transparent"></div>
        <p className="mt-4 text-zinc-500 dark:text-zinc-400 font-medium">Abrindo Centro do Jogo...</p>
      </div>
    );
  }

  if (error || !match) {
    return (
      <div className="text-center py-16">
        <div className="text-5xl mb-4">🏟️</div>
        <h3 className="text-xl font-bold">Jogo Não Encontrado</h3>
        <p className="text-zinc-500 mt-2">{error || "O jogo especificado não existe no banco de dados."}</p>
        <Link href="/" className="mt-4 inline-block bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2 rounded-xl text-sm font-semibold transition-all">
          Voltar ao Dashboard
        </Link>
      </div>
    );
  }

  const hasPrediction = !!match.prediction;
  const homeProb = match.prediction?.home_win_prob || 0;
  const drawProb = match.prediction?.draw_prob || 0;
  const awayProb = match.prediction?.away_win_prob || 0;

  return (
    <div className="space-y-6">
      {/* Breadcrumb */}
      <div className="text-xs text-zinc-400">
        <Link href="/" className="hover:underline">Dashboard</Link>
        <span className="mx-2">/</span>
        <span className="text-zinc-500">Jogo #{match.id}</span>
      </div>

      {/* Main Scoreboard */}
      <section className="relative rounded-3xl overflow-hidden bg-gradient-to-br from-zinc-900 to-zinc-950 p-6 sm:p-10 text-white shadow-xl">
        {match.is_g3_vs_z3 && (
          <div className="absolute right-0 top-0 bg-gradient-to-l from-amber-500 to-orange-500 text-white px-4 py-1.5 text-xs font-black uppercase tracking-wider rounded-bl-2xl shadow-md">
            Jogo Assimétrico (G3 vs Z3)
          </div>
        )}
        
        <div className="flex flex-col items-center gap-6 md:flex-row md:justify-between md:gap-4">
          {/* Home Team */}
          <div className="flex flex-col items-center gap-3 text-center md:flex-row md:text-left md:w-[35%]">
            {match.home_team_logo && (
              <img src={getProxiedImageUrl(match.home_team_logo)} className="w-16 h-16 sm:w-20 sm:h-20 object-contain p-2 bg-white/5 rounded-2xl" alt="" />
            )}
            <div>
              <h2 className="text-xl sm:text-2xl font-bold">{match.home_team}</h2>
              <span className="text-xs text-zinc-400">Casa</span>
            </div>
          </div>

          {/* Versus / Score */}
          <div className="flex flex-col items-center gap-1 md:w-[30%]">
            <span className="text-[10px] tracking-wider uppercase text-zinc-400 font-bold bg-white/5 px-2.5 py-0.5 rounded-full mb-1">
              Rodada {match.matchday || "N/A"}
            </span>
            {match.status === "NS" ? (
              <div className="text-2xl sm:text-3xl font-black text-emerald-400 px-4 py-1.5 bg-emerald-500/10 rounded-2xl">
                VS
              </div>
            ) : (
              <div className="flex items-center gap-4 text-3xl sm:text-4xl font-mono font-black bg-white/5 px-5 py-2 rounded-2xl">
                <span>{match.home_score}</span>
                <span className="text-zinc-500">-</span>
                <span>{match.away_score}</span>
              </div>
            )}
            <span className="text-xs text-zinc-400 mt-2 font-semibold">{match.status}</span>
          </div>

          {/* Away Team */}
          <div className="flex flex-col items-center gap-3 text-center md:flex-row-reverse md:text-right md:w-[35%]">
            {match.away_team_logo && (
              <img src={getProxiedImageUrl(match.away_team_logo)} className="w-16 h-16 sm:w-20 sm:h-20 object-contain p-2 bg-white/5 rounded-2xl" alt="" />
            )}
            <div>
              <h2 className="text-xl sm:text-2xl font-bold">{match.away_team}</h2>
              <span className="text-xs text-zinc-400">Fora</span>
            </div>
          </div>
        </div>

        {/* Venue/Referee bar */}
        <div className="mt-8 pt-6 border-t border-white/5 flex flex-wrap gap-4 items-center justify-between text-xs text-zinc-400">
          <div>📅 {formatMatchDate(match.match_date)}</div>
          <div>🏟️ {match.venue || "Estádio Desconhecido"}</div>
          {match.referee && <div>🏁 Árbitro: {match.referee}</div>}
        </div>
      </section>

      {/* Grid: Predictions & AI Analysis */}
      <div className="grid gap-6 md:grid-cols-3">
        {/* Bayesian Predictions column */}
        <div className="md:col-span-1 p-6 rounded-2xl border border-zinc-200/60 bg-white dark:border-zinc-800/60 dark:bg-zinc-900/40 space-y-6">
          <h3 className="font-bold text-lg border-b border-zinc-100 dark:border-zinc-800/80 pb-3 flex items-center gap-2">
            <span>🔮</span> Modelo de Previsão
          </h3>

          {!hasPrediction ? (
            <div className="text-center py-6 text-zinc-400 space-y-2">
              <span className="text-3xl">💤</span>
              <p className="text-sm font-medium">Nenhuma previsão estatística disponível.</p>
              <Link href="/admin" className="text-xs text-emerald-500 font-bold hover:underline">
                Gerar no Painel Admin
              </Link>
            </div>
          ) : (
            <div className="space-y-6">
              {/* Segemented probability bar */}
              <div className="space-y-2">
                <span className="text-xs font-semibold text-zinc-500">Probabilidade de Resultado</span>
                
                {/* Horizontal Bar Chart */}
                <div className="flex h-5 w-full rounded-full overflow-hidden shadow-inner text-[10px] font-black text-white text-center">
                  <div style={{ width: `${homeProb * 100}%` }} className="bg-gradient-to-r from-blue-500 to-cyan-500 flex items-center justify-center">
                    {homeProb > 0.15 && `${Math.round(homeProb * 100)}%`}
                  </div>
                  <div style={{ width: `${drawProb * 100}%` }} className="bg-zinc-400 flex items-center justify-center">
                    {drawProb > 0.15 && `${Math.round(drawProb * 100)}%`}
                  </div>
                  <div style={{ width: `${awayProb * 100}%` }} className="bg-gradient-to-r from-rose-500 to-pink-500 flex items-center justify-center">
                    {awayProb > 0.15 && `${Math.round(awayProb * 100)}%`}
                  </div>
                </div>

                {/* Legend */}
                <div className="flex items-center justify-between text-xs font-bold pt-1.5">
                  <span className="text-blue-500 flex items-center gap-1.5">
                    <span className="h-2 w-2 rounded-full bg-blue-500"></span> Vitória Casa
                  </span>
                  <span className="text-zinc-500 flex items-center gap-1.5">
                    <span className="h-2 w-2 rounded-full bg-zinc-400"></span> Empate
                  </span>
                  <span className="text-rose-500 flex items-center gap-1.5">
                    <span className="h-2 w-2 rounded-full bg-rose-500"></span> Vitória Fora
                  </span>
                </div>
              </div>

              {/* Goal Stats */}
              <div className="grid grid-cols-2 gap-4 pt-4 border-t border-zinc-100 dark:border-zinc-800/80">
                <div className="p-3 bg-zinc-50/50 dark:bg-zinc-900/30 rounded-xl border border-zinc-100 dark:border-zinc-800 text-center">
                  <span className="text-[10px] font-bold text-zinc-400 dark:text-zinc-500 block">Mais de 2.5 Gols</span>
                  <span className="text-xl font-extrabold text-zinc-900 dark:text-zinc-50 mt-1 block">
                    {match.prediction?.over_2_5_prob ? `${Math.round(match.prediction.over_2_5_prob * 100)}%` : "N/A"}
                  </span>
                </div>
                <div className="p-3 bg-zinc-50/50 dark:bg-zinc-900/30 rounded-xl border border-zinc-100 dark:border-zinc-800 text-center">
                  <span className="text-[10px] font-bold text-zinc-400 dark:text-zinc-500 block">Ambos Marcam</span>
                  <span className="text-xl font-extrabold text-zinc-900 dark:text-zinc-50 mt-1 block">
                    {match.prediction?.btts_prob ? `${Math.round(match.prediction.btts_prob * 100)}%` : "N/A"}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* AI Tactical Intelligence column */}
        <div className="md:col-span-2 p-6 rounded-2xl border border-zinc-200/60 bg-white dark:border-zinc-800/60 dark:bg-zinc-900/40 flex flex-col justify-between">
          <div className="space-y-4">
            <div className="flex items-center justify-between border-b border-zinc-100 dark:border-zinc-800/80 pb-3">
              <h3 className="font-bold text-lg flex items-center gap-2">
                <span>🤖</span> Inteligência Tática IA
              </h3>
              {match.ai_analysis && (
                <span className="text-[10px] font-semibold text-zinc-400 dark:text-zinc-500">
                  via {match.ai_analysis.provider} ({match.ai_analysis.model})
                </span>
              )}
            </div>

            <div className="min-h-[200px]">
              {!match.ai_analysis ? (
                <div className="flex flex-col items-center justify-center py-12 text-center space-y-4 h-full">
                  <span className="text-5xl">🧠</span>
                  <div>
                    <h4 className="font-bold text-sm">Sem Análise Tática Ainda</h4>
                    <p className="text-xs text-zinc-500 dark:text-zinc-400 max-w-sm mt-1">
                      Gere um relatório tático detalhado incluindo prévia, duelos e placar previsto usando nossos modelos de IA generativa.
                    </p>
                  </div>
                  <button
                    onClick={handleGenerateAnalysis}
                    disabled={analyzing}
                    className="rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs px-4 py-2.5 transition duration-200 flex items-center gap-2 shadow-md disabled:opacity-50"
                  >
                    {analyzing ? (
                      <>
                        <div className="h-3 w-3 animate-spin rounded-full border-2 border-white border-t-transparent"></div>
                        <span>Analisando Taticamente...</span>
                      </>
                    ) : (
                      <span>Gerar Análise de IA</span>
                    )}
                  </button>
                </div>
              ) : (
                <div className="prose dark:prose-invert max-w-none text-zinc-700 dark:text-zinc-300">
                  {renderMarkdown(match.ai_analysis.text)}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
