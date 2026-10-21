
import pandas as pd

ml = pd.read_csv(
    "dados_processados/isolation_forest_temporal.csv"
)

estatistico = pd.read_csv(
    "dados_processados/simulacao_retrospectiva.csv"
)

ml = ml.rename(columns={"ano_semana": "ano"})

comparacao = ml.merge(
    estatistico[
        ["ano", "semana", "possivel_alerta"]
    ],
    on=["ano", "semana"],
    how="inner"
)

comparacao["resultado_comparacao"] = "Nenhum sinalizou"

comparacao.loc[
    comparacao["possivel_anomalia"]
    & comparacao["possivel_alerta"],
    "resultado_comparacao"
] = "Ambos sinalizaram"

comparacao.loc[
    comparacao["possivel_anomalia"]
    & ~comparacao["possivel_alerta"],
    "resultado_comparacao"
] = "Somente Isolation Forest"

comparacao.loc[
    ~comparacao["possivel_anomalia"]
    & comparacao["possivel_alerta"],
    "resultado_comparacao"
] = "Somente método estatístico"

print("Resumo da comparação temporal:")
print(
    comparacao["resultado_comparacao"]
    .value_counts()
    .to_string()
)

print("\nComparação por ano:")
print(
    comparacao.groupby("ano").agg(
        semanas_comparadas=("semana", "count"),
        alertas_ml=("possivel_anomalia", "sum"),
        alertas_estatisticos=("possivel_alerta", "sum")
    ).to_string()
)

print("\nSemanas sinalizadas pelos dois métodos:")
print(
    comparacao[
        comparacao["resultado_comparacao"]
        == "Ambos sinalizaram"
    ][["ano", "semana", "quantidade"]]
    .sort_values(["ano", "semana"])
    .to_string(index=False)
)

comparacao.to_csv(
    "dados_processados/comparacao_temporal_estatistico.csv",
    index=False
)

print(
    "\nArquivo salvo: "
    "dados_processados/comparacao_temporal_estatistico.csv"
)
