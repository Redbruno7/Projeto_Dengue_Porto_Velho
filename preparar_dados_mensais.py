
from pathlib import Path

import pandas as pd

arquivo_entrada = Path(
    "dados_processados/casos_dengue_porto_velho.csv"
)

arquivo_saida = Path(
    "dados_processados/casos_mensais_risco.csv"
)

dados = pd.read_csv(arquivo_entrada)

dados["DT_SIN_PRI"] = pd.to_datetime(
    dados["DT_SIN_PRI"],
    errors="coerce"
)

# Mantém o período definido para a análise.
dados = dados[
    dados["DT_SIN_PRI"].between(
        "2016-01-01",
        "2025-12-31"
    )
].copy()

# Agrupa os casos por mês.
dados["mes"] = dados["DT_SIN_PRI"].dt.to_period("M")

mensal = (
    dados.groupby("mes")
    .size()
    .reset_index(name="quantidade_casos")
)

# Garante que todos os 120 meses estejam representados.
calendario = pd.period_range(
    start="2016-01",
    end="2025-12",
    freq="M"
)

mensal = (
    mensal.set_index("mes")
    .reindex(calendario, fill_value=0)
    .rename_axis("mes")
    .reset_index()
)

# Define as classes relativas de risco.
mensal["risco"] = pd.cut(
    mensal["quantidade_casos"],
    bins=[-float("inf"), 9, 30, float("inf")],
    labels=["Baixo", "Médio", "Alto"]
)

mensal["mes"] = mensal["mes"].astype(str)

arquivo_saida.parent.mkdir(
    parents=True,
    exist_ok=True
)

mensal.to_csv(
    arquivo_saida,
    index=False
)

print("Base mensal criada.")
print("Total de meses:", len(mensal))

print("\nDistribuição das classes:")
print(
    mensal["risco"]
    .value_counts()
    .reindex(["Baixo", "Médio", "Alto"], fill_value=0)
    .to_string()
)

print("\nPrimeiros meses:")
print(mensal.head(12).to_string(index=False))

print(f"\nArquivo salvo: {arquivo_saida}")
