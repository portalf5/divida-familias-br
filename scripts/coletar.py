"""
Coleta e análise — Endividamento das Famílias (BCB SGS 29038)
Gera: data/dados.json

Instalar: pip install pandas requests statsmodels scipy
Rodar:    python scripts/coletar.py
"""

import requests
import pandas as pd
import json
from datetime import datetime
from pathlib import Path

# ── séries do BCB ──────────────────────────────────────────────
SERIES = {
    "endividamento": 29038,
    "selic":         4189,
    "ipca":          433,
    "desemprego":    24369,
}

EVENTOS = [
    {"data": "2008-09-01", "label": "Crise financeira global"},
    {"data": "2011-07-01", "label": "Pico histórico pré-recessão"},
    {"data": "2014-12-01", "label": "Início da recessão brasileira"},
    {"data": "2016-05-01", "label": "Impeachment Dilma Rousseff"},
    {"data": "2020-03-01", "label": "Pandemia COVID-19"},
    {"data": "2020-08-01", "label": "Pico do auxílio emergencial"},
    {"data": "2022-08-01", "label": "Selic a 13,75% ao ano"},
    {"data": "2023-06-01", "label": "Crise Americanas / crédito"},
]

def fetch(codigo, nome):
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json"
    print(f"  baixando {nome} (SGS {codigo})...")
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    df = pd.DataFrame(r.json())
    df["data"] = pd.to_datetime(df["data"], dayfirst=True)
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    return df.set_index("data")["valor"].rename(nome)

def main():
    print("=== Coletando séries do BCB ===")
    series = [fetch(cod, nome) for nome, cod in SERIES.items()]
    df = pd.concat(series, axis=1).sort_index()
    df = df[df["endividamento"].notna()].resample("MS").mean()
    print(f"  {len(df)} meses: {df.index[0].strftime('%b/%Y')} → {df.index[-1].strftime('%b/%Y')}")

    # tendência (média móvel 12m como fallback; STL se statsmodels disponível)
    try:
        from statsmodels.tsa.seasonal import STL
        stl = STL(df["endividamento"].dropna(), period=12, robust=True).fit()
        tendencia = pd.Series(stl.trend, index=df["endividamento"].dropna().index)
        print("  decomposição STL concluída")
    except ImportError:
        tendencia = df["endividamento"].rolling(12, center=True).mean()
        print("  statsmodels ausente — usando média móvel")

    # correlações
    correlacoes = {}
    try:
        from scipy.stats import pearsonr
        for var in ["selic", "ipca", "desemprego"]:
            if var not in df.columns: continue
            correlacoes[var] = {}
            base = df[["endividamento", var]].dropna()
            for lag in [0, 1, 3, 6, 12]:
                x = base["endividamento"].iloc[lag:] if lag else base["endividamento"]
                y = base[var].iloc[:-lag] if lag else base[var]
                if len(x) < 10: continue
                r, p = pearsonr(x, y)
                correlacoes[var][f"lag_{lag}"] = {"r": round(r, 4), "p": round(p, 6)}
        print("  correlações calculadas")
    except ImportError:
        print("  scipy ausente — correlações ignoradas")

    # estatísticas
    s = df["endividamento"].dropna()
    stats = {
        "atual":      round(float(s.iloc[-1]), 2),
        "data_atual": s.index[-1].strftime("%b/%Y"),
        "media":      round(float(s.mean()), 2),
        "mediana":    round(float(s.median()), 2),
        "max":        round(float(s.max()), 2),
        "min":        round(float(s.min()), 2),
        "data_max":   s.idxmax().strftime("%Y-%m"),
        "data_min":   s.idxmin().strftime("%Y-%m"),
        "var_total":  round(float(s.iloc[-1] - s.iloc[0]), 2),
    }

    # montar payload
    serie_json = []
    for idx, row in df.iterrows():
        rec = {"data": idx.strftime("%Y-%m-%d")}
        for col in df.columns:
            v = row[col]
            rec[col] = None if pd.isna(v) else round(float(v), 4)
        serie_json.append(rec)

    stl_json = [
        {"data": idx.strftime("%Y-%m-%d"),
         "tendencia": None if pd.isna(v) else round(float(v), 4)}
        for idx, v in tendencia.items()
    ]

    payload = {
        "gerado_em":   datetime.now().isoformat(),
        "fonte":       "Banco Central do Brasil — SGS 29038",
        "licenca":     "ODbL",
        "serie":       serie_json,
        "stl":         stl_json,
        "eventos":     EVENTOS,
        "correlacoes": correlacoes,
        "estatisticas":stats,
    }

    Path("data").mkdir(exist_ok=True)
    with open("data/dados.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print("  ✓ data/dados.json salvo")
    print(f"\n  Endividamento atual: {stats['atual']}% ({stats['data_atual']})")
    print(f"  Máximo histórico:    {stats['max']}% ({stats['data_max']})")
    print(f"  Variação total:      {stats['var_total']:+.2f} p.p.")

if __name__ == "__main__":
    main()
