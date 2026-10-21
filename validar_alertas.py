
import pandas as pd

# Carrega os arquivos utilizados na análise
casos = pd.read_csv(
    "dados_processados/casos_por_semana.csv"
)

estatistico = pd.read_csv(
    "dados_processados/simulacao_retrospectiva.csv"
)

ml = pd.read_csv(
    "dados_processados/isolation_forest_temporal.csv"
)

# Seleciona os anos de interesse
casos = casos[
    casos["ano_semana"].isin([2022, 2023])
].copy()

estatistico = estatistico[
    estatistico["ano"].isin([2022, 2023])
].copy()

ml = ml[
    ml["ano_semana"].isin([2022, 2023])
].copy()

# Junta os resultados por ano e semana
relatorio = casos.merge(
    estatistico[
        [
            "ano",
            "semana",
            "media_historica",
            "limite_alerta",
            "possivel_alerta"
        ]
    ],
    left_on=["ano_semana", "semana"],
    right_on=["ano", "semana"],
    how="left"
)

relatorio = relatorio.merge(
    ml[
        ["ano_semana", "semana", "possivel_anomalia"]
    ],
    on=["ano_semana", "semana"],
    how="left"
)

# Preenche semanas sem avaliação estatística
relatorio["possivel_alerta"] = (
    relatorio["possivel_alerta"].fillna(False).astype(bool)
)

relatorio["possivel_anomalia"] = (
    relatorio["possivel_anomalia"].fillna(False).astype(bool)
)

# Identifica a semana de maior quantidade em cada ano
picos = (
    relatorio.loc[
        relatorio.groupby("ano_semana")["quantidade"].idxmax(),
        ["ano_semana", "semana", "quantidade"]
    ]
    .rename(columns={
        "semana": "semana_pico",
        "quantidade": "casos_no_pico"
    })
)

relatorio = relatorio.merge(
    picos,
    on="ano_semana",
    how="left"
)

relatorio["distancia_do_pico"] = (
    relatorio["semana"] - relatorio["semana_pico"]
)

# Classifica o momento dos alertas em relação ao pico
def classificar_momento(linha):
    if not linha["possivel_alerta"] and not linha["possivel_anomalia"]:
        return "Sem alerta"

    if linha["semana"] < linha["semana_pico"]:
        return "Antes do pico"

    if linha["semana"] == linha["semana_pico"]:
        return "Na semana do pico"

    return "Depois do pico"

relatorio["momento_alerta"] = relatorio.apply(
    classificar_momento,
    axis=1
)

# Organiza as colunas
colunas = [
    "ano_semana",
    "semana",
    "quantidade",
    "media_historica",
    "limite_alerta",
    "possivel_alerta",
    "possivel_anomalia",
    "semana_pico",
    "casos_no_pico",
    "distancia_do_pico",
    "momento_alerta"
]

relatorio = relatorio[colunas].sort_values(
    ["ano_semana", "semana"]
)

# Salva o relatório completo
relatorio.to_csv(
    "dados_processados/validacao_alertas_2022_2023.csv",
    index=False
)

# Exibe somente as semanas com algum alerta
alertas = relatorio[
    relatorio["possivel_alerta"]
    | relatorio["possivel_anomalia"]
]

print("Resumo do momento dos alertas:")
print(
    alertas.groupby(
        ["ano_semana", "momento_alerta"]
    ).size().to_string()
)

print("\nPrimeiras semanas sinalizadas:")
print(
    alertas[
        [
            "ano_semana",
            "semana",
            "quantidade",
            "limite_alerta",
            "possivel_alerta",
            "possivel_anomalia",
            "momento_alerta"
        ]
    ].head(20).to_string(index=False)
)

print(
    "\nArquivo salvo: "
    "dados_processados/validacao_alertas_2022_2023.csv"
)
