#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Algoritmo de IA para:
- Buscar classificações (standings) e próximos jogos das ligas:
  Alemanha (Bundesliga), Inglaterra (Premier League), França (Ligue 1),
  Holanda (Eredivisie), Brasil (Série A) e Espanha (La Liga).
- Calcular probabilidades de vitória para cada jogo com base na classificação atual
  (modelo simples Bradley‑Terry com empate adaptativo).
- Destacar confrontos Top‑3 vs Bottom‑3.
- Salvar tabelas em CSV **e também em FIGURAS (PNG)** para fácil compartilhamento.

Fonte dos dados: football-data.org v4 (requer API key no header X-Auth-Token).
"""

from __future__ import annotations
import os
import time
import math
import json
import sys
import logging
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta, timezone

import requests
import pandas as pd
import numpy as np

# Para figuras
import matplotlib
matplotlib.use("Agg")  # backend sem GUI
import matplotlib.pyplot as plt

API_BASE = "https://api.football-data.org/v4"
API_TOKEN = os.getenv("FOOTBALL_DATA_API_KEY", "").strip()

# Liga -> código football-data.org v4
LEAGUES = {
    "Alemanha - Bundesliga": "BL1",
    "Inglaterra - Premier League": "PL",
    "França - Ligue 1": "FL1",
    "Holanda - Eredivisie": "DED",
    "Brasil - Série A": "BSA",
    "Espanha - La Liga": "PD",
}

HEADERS = {"X-Auth-Token": API_TOKEN} if API_TOKEN else {}

# --- Utilidades de request com retry robusto ---
def _request_json(url: str, params: dict | None = None, max_retries: int = 4, backoff: float = 1.7):
    if not API_TOKEN:
        raise RuntimeError("FOOTBALL_DATA_API_KEY não encontrada no ambiente.")
    last_err: Optional[Exception] = None
    for i in range(max_retries):
        try:
            r = requests.get(url, headers=HEADERS, params=params, timeout=30)
        except requests.RequestException as e:
            last_err = e
            time.sleep(backoff ** (i + 1))
            continue

        if r.status_code == 429:
            retry_after = r.headers.get("Retry-After")
            try:
                wait_s = float(retry_after) if retry_after is not None else backoff ** (i + 1)
            except ValueError:
                wait_s = backoff ** (i + 1)
            last_err = requests.HTTPError("429 Too Many Requests (rate limit atingido).")
            time.sleep(wait_s)
            continue

        if r.status_code >= 400:
            last_err = requests.HTTPError(f"HTTP {r.status_code}: {r.text[:200]}")
            time.sleep(backoff ** (i + 1))
            continue

        try:
            return r.json()
        except ValueError as e:
            last_err = e
            time.sleep(backoff ** (i + 1))
            continue

    raise last_err or RuntimeError("Falha após múltiplas tentativas de requisição.")

# --- Standing & Fixtures ---
def get_total_standing(league_code: str) -> pd.DataFrame:
    """Retorna a standing TOTAL da liga como DataFrame."""
    url = f"{API_BASE}/competitions/{league_code}/standings"
    data = _request_json(url)
    standings = data.get("standings", [])
    total = next((s for s in standings if s.get("type") == "TOTAL"), None)
    if not total:
        return pd.DataFrame()
    rows = []
    for row in total.get("table", []):
        team = row.get("team", {})
        rows.append({
            "position": row.get("position"),
            "team_id": team.get("id"),
            "team": team.get("name"),
            "tla": team.get("tla"),
            "played": row.get("playedGames"),
            "won": row.get("won"),
            "draw": row.get("draw"),
            "lost": row.get("lost"),
            "gf": row.get("goalsFor"),
            "ga": row.get("goalsAgainst"),
            "gd": row.get("goalDifference"),
            "points": row.get("points"),
            "form": row.get("form"),
        })
    df = pd.DataFrame(rows)
    return df

def get_upcoming_matches(
    league_code: str,
    days_ahead: int = 10,
    status: str = "SCHEDULED,TIMED"
) -> pd.DataFrame:
    """Retorna próximos jogos da liga no intervalo [hoje, hoje+days_ahead]."""
    url = f"{API_BASE}/competitions/{league_code}/matches"
    today = datetime.now(timezone.utc).date()
    date_from = today.isoformat()
    date_to = (today + timedelta(days=days_ahead)).isoformat()
    params = {"status": status, "dateFrom": date_from, "dateTo": date_to}
    data = _request_json(url, params=params)
    rows = []
    for m in data.get("matches", []):
        home = m.get("homeTeam", {})
        away = m.get("awayTeam", {})
        rows.append({
            "match_id": m.get("id"),
            "utcDate": m.get("utcDate"),
            "status": m.get("status"),
            "matchday": m.get("matchday"),
            "home_id": home.get("id"),
            "home": home.get("name"),
            "home_tla": home.get("tla"),
            "away_id": away.get("id"),
            "away": away.get("name"),
            "away_tla": away.get("tla"),
            "venue": m.get("venue"),
        })
    return pd.DataFrame(rows)

# --- Modelo de probabilidade de resultado (simples e explicável) ---
def _league_strengths_from_table(table: pd.DataFrame) -> pd.DataFrame:
    """
    Constrói um 'rating' por time a partir da classificação atual combinando:
      - Pontos por jogo (PPG) (peso 0.7)
      - Saldo por jogo (GDG) (peso 0.3)
    Normaliza por z-score na liga e aplica uma pequena suavização.
    """
    df = table.copy()
    df["ppg"] = df["points"] / df["played"].replace(0, np.nan)
    df["gdg"] = df["gd"] / df["played"].replace(0, np.nan)
    # Preenche possíveis NaN (início de temporada) com medianas 0
    df["ppg"] = df["ppg"].fillna(df["ppg"].median() if not pd.isna(df["ppg"].median()) else 0.0)
    df["gdg"] = df["gdg"].fillna(0.0)
    # Z-score
    for col in ["ppg","gdg"]:
        mu = df[col].mean()
        sd = df[col].std(ddof=0) or 1.0
        df[f"z_{col}"] = (df[col] - mu) / sd
    # Rating combinado
    df["rating"] = 0.7 * df["z_ppg"] + 0.3 * df["z_gdg"]
    # Suavização leve para extremos
    df["rating"] = df["rating"].clip(lower=df["rating"].quantile(0.05), upper=df["rating"].quantile(0.95))
    return df[["team_id","team","position","points","played","gd","rating"]]

def _bt_probabilities(home_r: float, away_r: float, base_draw: float = 0.24, k: float = 1.20, home_adv: float = 0.15) -> tuple[float,float,float]:
    """
    Bradley-Terry logístico com empate adaptativo:
      delta = (home_r - away_r) + home_adv
      p_home_raw = sigmoid(k * delta)
      p_away_raw = 1 - p_home_raw
      p_draw_raw = base_draw * exp(-|delta|)
    Normaliza para P_home + P_draw + P_away = 1
    Retorna: (p_home, p_draw, p_away)
    """
    delta = (home_r - away_r) + home_adv
    p_home_raw = 1 / (1 + math.exp(-k * delta))
    p_away_raw = 1 - p_home_raw
    p_draw_raw = base_draw * math.exp(-abs(delta))
    z = p_home_raw + p_away_raw + p_draw_raw  # = 1 + p_draw_raw
    return p_home_raw / z, p_draw_raw / z, p_away_raw / z

def compute_match_probs(fixtures: pd.DataFrame, strengths: pd.DataFrame) -> pd.DataFrame:
    """Anexa colunas de probabilidade e flags Top3 vs Bottom3 aos jogos."""
    st_by_id = strengths.set_index("team_id").to_dict(orient="index")
    # Bottom-3 são as três piores posições (posição máxima depende do tamanho da liga)
    n_teams = int(strengths["position"].max())
    bottom_cut = n_teams - 2  # ex.: 20 times -> bottom 3 = 18,19,20

    out_rows = []
    for _, row in fixtures.iterrows():
        home = st_by_id.get(row["home_id"])
        away = st_by_id.get(row["away_id"])
        if not home or not away:
            continue
        p_home, p_draw, p_away = _bt_probabilities(home["rating"], away["rating"])
        flag_top_vs_bottom = (home["position"] <= 3 and away["position"] >= bottom_cut) or \
                             (away["position"] <= 3 and home["position"] >= bottom_cut)
        categoria = "Top-3 vs Bottom-3" if flag_top_vs_bottom else ""
        out_rows.append({
            "utcDate": row["utcDate"],
            "matchday": row["matchday"],
            "home": home["team"],
            "home_pos": int(home["position"]),
            "away": away["team"],
            "away_pos": int(away["position"]),
            "P(Home)": round(p_home, 3),
            "P(Draw)": round(p_draw, 3),
            "P(Away)": round(p_away, 3),
            "ALERTA": categoria,
        })
    df = pd.DataFrame(out_rows).sort_values(["ALERTA","utcDate","matchday"], ascending=[False, True, True]).reset_index(drop=True)
    return df

# --- Utilidades para FIGURAS ---
def _truncate(s: str, n: int = 22) -> str:
    if s is None:
        return ""
    return (s[: n-1] + "…") if len(s) > n else s

def save_dataframe_as_table_image(df: pd.DataFrame, title: str, out_path: str, max_rows: int = 30):
    """
    Salva um DataFrame como imagem (PNG) usando matplotlib.table.
    Regras: um gráfico por figura, sem definir cores específicas.
    """
    df_to_show = df.copy().head(max_rows)
    # Trunca possíveis colunas de texto longas
    for col in df_to_show.select_dtypes(include=["object"]).columns:
        df_to_show[col] = df_to_show[col].astype(str).map(lambda x: _truncate(x, 28))

    n_rows, n_cols = df_to_show.shape
    # Tenta ajustar tamanho: 0.5" por coluna e 0.45" por linha, com limites
    fig_w = max(6.0, min(18.0, n_cols * 0.8 + 2.0))
    fig_h = max(3.0, min(24.0, n_rows * 0.45 + 1.6))

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.axis("off")
    tbl = ax.table(cellText=df_to_show.values, colLabels=df_to_show.columns, loc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8)
    tbl.scale(1, 1.2)

    # Título
    fig.suptitle(title, fontsize=12, fontweight="bold", y=0.98)
    fig.tight_layout(rect=[0.02, 0.02, 0.98, 0.95])
    fig.savefig(out_path, dpi=200)
    plt.close(fig)

def save_points_bar_chart(standings: pd.DataFrame, league_title: str, out_path: str):
    """
    Salva um gráfico de barras simples com os pontos por time, ordenado por pontos.
    Um gráfico por figura, sem definir cores específicas.
    """
    df = standings[["team", "points"]].copy().sort_values("points", ascending=True)
    fig, ax = plt.subplots(figsize=(8, max(4.0, len(df) * 0.35)))
    ax.barh(df["team"], df["points"])  # sem setar cores
    ax.set_xlabel("Pontos")
    ax.set_ylabel("Time")
    ax.set_title(f"{league_title} — Pontos")
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)

def run_pipeline(days_ahead: int = 10, out_dir: str = "out", make_figures: bool = False, only: Optional[str] = None):
    os.makedirs(out_dir, exist_ok=True)
    summary = []
    leagues_iter = LEAGUES.items()

    # Permitir rodar só uma liga via --only (pode ser o código ou parte do nome)
    if only:
        only_lower = only.lower()
        leagues_iter = [(name, code) for name, code in LEAGUES.items()
                        if only_lower in name.lower() or only_lower == code.lower()]

    for league_name, code in leagues_iter:
        print(f"\n=== {league_name} ({code}) ===")
        try:
            standings = get_total_standing(code)
            if standings.empty:
                print("Sem standings para esta liga.")
                continue
            strengths = _league_strengths_from_table(standings)
            fixtures = get_upcoming_matches(code, days_ahead=days_ahead)
            if fixtures.empty:
                print("Sem jogos agendados no período.")
                continue
            probs = compute_match_probs(fixtures, strengths)

            # CSVs
            standings_csv = os.path.join(out_dir, f"standings_{code}.csv")
            fixtures_csv = os.path.join(out_dir, f"fixtures_probs_{code}.csv")
            standings.to_csv(standings_csv, index=False)
            probs.to_csv(fixtures_csv, index=False)

            # FIGURAS (opcional)
            if make_figures:
                # Tabela de classificação (PNG)
                standings_png = os.path.join(out_dir, f"standings_{code}.png")
                standings_for_img = standings[["position","team","played","points","gd","form"]].copy()
                save_dataframe_as_table_image(standings_for_img, f"{league_name} — Classificação", standings_png)

                # Gráfico de barras de pontos
                points_png = os.path.join(out_dir, f"points_{code}.png")
                save_points_bar_chart(standings, league_title=league_name, out_path=points_png)

                # Tabela de jogos com probabilidades (até 30 linhas)
                fixtures_png = os.path.join(out_dir, f"fixtures_probs_{code}.png")
                probs_for_img = probs[["utcDate","matchday","home","home_pos","away","away_pos","P(Home)","P(Draw)","P(Away)","ALERTA"]].copy()
                save_dataframe_as_table_image(probs_for_img, f"{league_name} — Jogos (próximos {days_ahead} dias)", fixtures_png)

            # Resumo de alertas
            alerta = probs[probs["ALERTA"] == "Top-3 vs Bottom-3"]
            print(f"{len(alerta)} confronto(s) Top-3 vs Bottom-3 nas próximas {days_ahead} dias.")
            summary.append({
                "league": league_name,
                "code": code,
                "qtd_alertas": int(len(alerta)),
                "csv_standings": f"standings_{code}.csv",
                "csv_fixtures": f"fixtures_probs_{code}.csv",
                **({"png_standings": f"standings_{code}.png",
                    "png_points": f"points_{code}.png",
                    "png_fixtures": f"fixtures_probs_{code}.png"} if make_figures else {})
            })
        except Exception as e:
            print(f"Falha em {league_name} ({code}): {e}")
            continue
    if summary:
        pd.DataFrame(summary).to_csv(os.path.join(out_dir, "resumo_ligas.csv"), index=False)
        print("\nArquivos gerados em:", out_dir)
    else:
        print("\nNenhuma liga processada com sucesso.")

# --- Execução via CLI ---
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Top-3 vs Bottom-3 + Probabilidades por liga (football-data.org)")
    parser.add_argument("--days", type=int, default=10, help="Janela de dias à frente para buscar jogos (default: 10)")
    parser.add_argument("--out", type=str, default="out", help="Pasta de saída para CSVs/PNGs (default: out)")
    parser.add_argument("--figures", action="store_true", help="Se presente, também salva figuras (PNG) das tabelas e gráficos.")
    parser.add_argument("--only", type=str, default=None, help="Processa apenas a liga cujo nome/código contenha este texto (ex.: 'PL' ou 'La Liga').")
    args = parser.parse_args()

    run_pipeline(days_ahead=args.days, out_dir=args.out, make_figures=args.figures, only=args.only)
