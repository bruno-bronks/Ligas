# Streamlit — Futebol Dashboard (Top‑3 × Bottom‑3)

Este app Streamlit consome diretamente a API do football-data.org usando sua API key e calcula probabilidades (Bradley‑Terry) para destacar confrontos Top‑3 × Bottom‑3. Inclui Champions League (opcional, ranking global).

## Como rodar (Windows PowerShell)

```powershell
# 1) Crie e ative o ambiente
py -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) Instale dependências
pip install -r requirements_streamlit.txt

# 3) Defina sua API key (ou digite no app)
$env:FOOTBALL_DATA_API_KEY = "SUA_CHAVE_AQUI"

# 4) Rode o app
streamlit run streamlit_app.py
```

Abra o link que o Streamlit mostrar (ex.: http://localhost:8501).

## Observações

- Se a API limitar (HTTP 429), espere alguns segundos e atualize; o app usa cache de 60s por requisição.
- A janela de dias pode influenciar o número de chamadas; tente 7–10 para reduzir rate limit.
- Você pode digitar a chave no campo lateral caso não queira usar variável de ambiente.
