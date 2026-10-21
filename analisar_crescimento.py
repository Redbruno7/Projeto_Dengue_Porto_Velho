
import pandas as pd

dados = pd.read_csv(
    "dados_processados/casos_por_semana.csv"
)

dados = dados[
    dados["ano_semana"].isin([2022, 2023])
].copy()

dados = dados.sort_values(
    ["ano_semana", "semana"]
)

dados["casos_semana_anterior"] = (
    dados.groupby("ano_semana")["quantidade"].shift(1)
)

dados["variacao_semanal"] = (
    dados["quantidade"] - dados["casos_semana_anterior"]
)

dados["media_3_semanas"] = (
    dados.groupby("ano_semana")["quantidade"]
    .transform(
        lambda serie: serie.rolling(
            window=3,
            min_periods=3
        ).mean()
    )
)

dados["media_3_semanas_anterior"] = (
    dados.groupby("ano_semana")["media_3_semanas"].shift(1)
)

dados["aumento_sustentado"] = (
    (dados["media_3_semanas"] > dados["media_3_semanas_anterior"])
    & (dados["variacao_semanal"] > 0)
)

for ano in [2022, 2023]:
    recorte = dados[dados["ano_semana"] == ano].copy()

    print(f"\nAno {ano}: primeiras semanas com aumento")

    print(
        recorte[
            recorte["aumento_sustentado"]
        ][
            [
                "semana",
                "quantidade",
                "variacao_semanal",
                "media_3_semanas"
            ]
        ].head(10).to_string(index=False)
    )

dados.to_csv(
    "dados_processados/analise_crescimento.csv",
    index=False
)

print("\nArquivo salvo: dados_processados/analise_crescimento.csv")
