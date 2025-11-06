# streamlit_app.py
# -*- coding: utf-8 -*-
import os
import time
import math
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple, List, Dict

import requests
import pandas as pd
import numpy as np
import streamlit as st

# =========================
# Configuração da página
# =========================
st.set_page_config(
    page_title="Futebol Dashboard — Top-3 × Bottom-3",
    page_icon="⚽",
    layout="wide",
)

# Pequeno tema/estilo
st.markdown(
    """
    <style>
    .small-note { color: rgba(255,255,255,0.65); font-size: 12px; }
    .ok-badge { display:inline-block; padding:2px 8px; border:1px solid #7dd3fc; border-radius:999px; color:#7dd3fc; font-weight:600; font-size:12px; }
    .warn-badge { display:inline-block; padding:2px 8px; border:1px solid #fde68a; border-radius:999px; color:#fde68a; font-weight:600; font-size:12px; }
    </style>
    """,
    unsafe_allow_html=True,
)

TIMEZONE = "America/Sao_Paulo"

# =========================
# Configurações iniciais
# =========================
BASE_LEAGUES = {
    "Alemanha - Bundesliga": "BL1",
    "Inglaterra - Premier League": "PL",
    "França - Ligue 1": "FL1",
    "Holanda - Eredivisie": "DED",
    "Brasil - Série A": "BSA",
    "Espanha - La Liga": "PD",
}
ALL_LEAGUES = {**BASE_LEAGUES, "Champions League": "CL"}

API_BASE = "https://api.football-data.org/v4"

@st.cache_data(show_spinner=False, ttl=60)
def _request_json(url: str, token: str, params: dict | None = None, max_retries: int = 4, backoff: float = 1.7):
    """Request com retry e cache simples (TTL=60s)."""
    headers = {"X-Auth-Token": token} if token else {}
    last_err: Optional[Exception] = None
    for i in range(max_retries):
        try:
            r = requests.get(url, headers=headers, params=params, timeout=30)
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
            last_err = requests.HTTPError("429 Too Many Requests (rate limit).")
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

def get_total_standing(token: str, league_code: str) -> pd.DataFrame:
    """Tabela TOTAL da liga. Em CL, cria ranking global pontos->gd->gf."""
    url = f"{API_BASE}/competitions/{league_code}/standings"
    data = _request_json(url, token=token)
    standings = data.get("standings", []) or []

    tables = [b for b in standings if b.get("table")]
    tables = sorted(tables, key=lambda b: (b.get("type") != "TOTAL",))

    rows = []
    for block in tables:
        for row in block.get("table", []):
            team = row.get("team", {}) or {}
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

    if league_code == "CL" and not df.empty:
        df = df.copy()
        df["points"] = df["points"].astype(int)
        df["gd"] = df["gd"].astype(int)
        df["gf"] = df["gf"].astype(int)
        df = df.sort_values(["points", "gd", "gf", "team"], ascending=[False, False, False, True]).reset_index(drop=True)
        df["position"] = np.arange(1, len(df) + 1)

    return df

def get_upcoming_matches(token: str,
                         league_code: str,
                         date_from: Optional[str] = None,
                         date_to: Optional[str] = None,
                         days_ahead: int = 10,
                         status: str = "SCHEDULED,TIMED") -> pd.DataFrame:
    """Próximos jogos na janela informada (ou hoje + N dias)."""
    url = f"{API_BASE}/competitions/{league_code}/matches"
    if date_from is None or date_to is None:
        today = datetime.now(timezone.utc).date()
        date_from = date_from or today.isoformat()
        date_to = date_to or (today + timedelta(days=days_ahead)).isoformat()
    params = {"status": status, "dateFrom": date_from, "dateTo": date_to}
    data = _request_json(url, token=token, params=params)

    rows = []
    for m in data.get("matches", []) or []:
        home = m.get("homeTeam", {}) or {}
        away = m.get("awayTeam", {}) or {}
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

# ====== Probabilidades ======
def _league_strengths_from_table(table: pd.DataFrame) -> pd.DataFrame:
    if table.empty:
        return pd.DataFrame(columns=["team_id","team","position","points","played","gd","rating"])
    df = table.copy()
    df["played"] = df["played"].replace(0, np.nan)
    df["ppg"] = df["points"] / df["played"]
    df["gdg"] = df["gd"] / df["played"]
    df["ppg"] = df["ppg"].fillna(df["ppg"].median() if not pd.isna(df["ppg"].median()) else 0.0)
    df["gdg"] = df["gdg"].fillna(0.0)
    for col in ["ppg","gdg"]:
        mu = df[col].mean()
        sd = df[col].std(ddof=0) or 1.0
        df[f"z_{col}"] = (df[col] - mu) / sd
    df["rating"] = 0.7 * df["z_ppg"] + 0.3 * df["z_gdg"]
    df["rating"] = df["rating"].clip(lower=df["rating"].quantile(0.05), upper=df["rating"].quantile(0.95))
    return df[["team_id","team","position","points","played","gd","rating"]]

def _bt_probabilities(home_r: float, away_r: float,
                      base_draw: float = 0.24, k: float = 1.20, home_adv: float = 0.15) -> Tuple[float,float,float]:
    delta = (home_r - away_r) + home_adv
    p_home_raw = 1 / (1 + math.exp(-k * delta))
    p_away_raw = 1 - p_home_raw
    p_draw_raw = base_draw * math.exp(-abs(delta))
    z = p_home_raw + p_away_raw + p_draw_raw
    return p_home_raw / z, p_draw_raw / z, p_away_raw / z

def compute_match_probs(fixtures: pd.DataFrame, strengths: pd.DataFrame) -> pd.DataFrame:
    if fixtures.empty or strengths.empty:
        return pd.DataFrame(columns=[
            "utcDate","matchday","home","home_pos","away","away_pos","P(Home)","P(Draw)","P(Away)","ALERTA"
        ])
    st_by_id = strengths.set_index("team_id").to_dict(orient="index")
    n_teams = int(strengths["position"].max())
    bottom_cut = n_teams - 2

    out_rows = []
    for _, row in fixtures.iterrows():
        home = st_by_id.get(row["home_id"])
        away = st_by_id.get(row["away_id"])
        if not home or not away: 
            continue
        p_home, p_draw, p_away = _bt_probabilities(home["rating"], away["rating"])
        flag_top_vs_bottom = (home["position"] <= 3 and away["position"] >= bottom_cut) or \
                             (away["position"] <= 3 and home["position"] >= bottom_cut)
        categoria = "⚠️ Top-3 × Bottom-3" if flag_top_vs_bottom else ""
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

def fmt_date_br(iso_str: str) -> str:
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z","+00:00"))
    except Exception:
        return iso_str
    return dt.astimezone(timezone.utc).strftime("%d/%m %H:%M")  # simples

# =========================
# Barra lateral (controles)
# =========================
st.sidebar.title("⚙️ Controles")

api_key_input = st.sidebar.text_input("API Key (football-data.org)", type="password", help="Você também pode usar a variável de ambiente FOOTBALL_DATA_API_KEY.")
api_key_env = os.getenv("FOOTBALL_DATA_API_KEY", "").strip()
API_TOKEN = api_key_input.strip() or api_key_env

if not API_TOKEN:
    st.sidebar.warning("Defina a API Key (campo acima) ou configure FOOTBALL_DATA_API_KEY no ambiente.")

include_cl = st.sidebar.checkbox("Incluir Champions League (CL)", value=True)

leagues_dict = {**BASE_LEAGUES, **({"Champions League": "CL"} if include_cl else {})}
leagues = st.sidebar.multiselect(
    "Ligas para exibir", 
    options=list(leagues_dict.keys()),
    default=list(leagues_dict.keys()),
)

days = st.sidebar.slider("Dias à frente", min_value=1, max_value=30, value=10, step=1)
date_from = st.sidebar.date_input("Data inicial (opcional)", value=None, format="YYYY-MM-DD")
date_to = st.sidebar.date_input("Data final (opcional)", value=None, format="YYYY-MM-DD")

colA, colB = st.sidebar.columns(2)
refresh = colA.button("🔄 Atualizar")
auto_every = colB.number_input("Auto (s)", min_value=30, max_value=600, value=180, step=30, help="Atualiza automaticamente a cada N segundos (experimental).")
auto_on = st.sidebar.toggle("Auto‑refresh", value=False, help="Ativa atualização automática (experimental).")

if auto_on:
    st.experimental_rerun  # linter

# =========================
# Cabeçalho
# =========================
st.title("Futebol Dashboard — Top‑3 × Bottom‑3")
st.caption("Ligas: Bundesliga, Premier League, Ligue 1, Eredivisie, Brasileirão A, La Liga e Champions League. Probabilidades por Bradley‑Terry (heurístico).")

# Auto-refresh experimental
if auto_on and API_TOKEN:
    st.experimental_singleton.clear()  # não afeta cache_data, apenas exemplo
    st_autorefresh = st.experimental_rerun  # placeholder
    st.experimental_set_query_params(ts=str(int(time.time())))  # força recarregar
    # Nota: streamlit_autorefresh oficial é st.experimental_memo? feature antiga; aqui usamos botões manualmente

if refresh:
    st.cache_data.clear()

# =========================
# Carregamento e Exibição
# =========================
if not leagues:
    st.info("Selecione ao menos uma liga na barra lateral.")
    st.stop()

# Calcula janela de datas
date_from_str = None
date_to_str = None
if date_from:
    date_from_str = str(date_from)
if date_to:
    date_to_str = str(date_to)
if date_from_str and not date_to_str:
    try:
        d0 = datetime.fromisoformat(date_from_str).date()
        date_to_str = (d0 + timedelta(days=days)).isoformat()
    except Exception:
        date_to_str = None

# Loop por liga selecionada
for lg_name in leagues:
    code = leagues_dict[lg_name]
    st.markdown(f"### {lg_name} ({code})")
    if not API_TOKEN:
        st.warning("Informe uma API Key para carregar os dados desta liga.")
        continue

    with st.spinner("Carregando standings e jogos..."):
        try:
            standings = get_total_standing(API_TOKEN, code)
            strengths = _league_strengths_from_table(standings) if not standings.empty else pd.DataFrame()
            fixtures = get_upcoming_matches(API_TOKEN, code, date_from=date_from_str, date_to=date_to_str, days_ahead=days)
            probs = compute_match_probs(fixtures, strengths) if not fixtures.empty else pd.DataFrame()
        except Exception as e:
            st.error(f"Falha ao obter dados: {e}")
            continue

    # Layout em 2 colunas
    c1, c2 = st.columns(2)

    # Classificação
    with c1:
        st.markdown("**Classificação**")
        if standings.empty:
            st.info("Sem standings para esta liga.")
        else:
            show_cols = ["position","team","played","points","gd","form"]
            st.dataframe(standings[show_cols], use_container_width=True, hide_index=True)
            # download CSV
            st.download_button(
                "⬇️ Baixar CSV (Classificação)",
                file_name=f"standings_{code}.csv",
                mime="text/csv",
                data=standings.to_csv(index=False).encode("utf-8"),
            )

    # Jogos + Probabilidades
    with c2:
        st.markdown(f"**Próximos jogos ({days} dias)**")
        if fixtures.empty:
            st.info("Sem jogos agendados no período.")
        else:
            if probs.empty:
                st.info("Não foi possível calcular probabilidades (dados insuficientes).")
                df_show = fixtures.copy()
                df_show["Data (BR)"] = df_show["utcDate"].map(fmt_date_br)
                show_cols = ["Data (BR)","matchday","home","away"]
                st.dataframe(df_show[show_cols], use_container_width=True, hide_index=True)
            else:
                df_show = probs.copy()
                df_show["Data (BR)"] = df_show["utcDate"].map(fmt_date_br)
                df_show["P(Home)%"] = (df_show["P(Home)"]*100).round(0).astype(int)
                df_show["P(Draw)%"] = (df_show["P(Draw)"]*100).round(0).astype(int)
                df_show["P(Away)%"] = (df_show["P(Away)"]*100).round(0).astype(int)
                show_cols = ["Data (BR)","matchday","home","home_pos","away","away_pos","P(Home)%","P(Draw)%","P(Away)%","ALERTA"]
                st.dataframe(df_show[show_cols], use_container_width=True, hide_index=True)
                # download CSV
                st.download_button(
                    "⬇️ Baixar CSV (Jogos + Prob.)",
                    file_name=f"fixtures_probs_{code}.csv",
                    mime="text/csv",
                    data=df_show[show_cols].to_csv(index=False).encode("utf-8"),
                )

    st.markdown("---")

st.markdown(
    '<div class="small-note">Probabilidades são heurísticas baseadas na classificação atual (PPG/GDG → z-score → Bradley‑Terry). Resultados reais podem divergir.</div>',
    unsafe_allow_html=True,
)
