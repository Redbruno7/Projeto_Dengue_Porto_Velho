import pandas as pd

arquivo_ml = "dados_processados/resultado_isolation_forest.csv"
arquivo_estatistico = "dados_processados/simulacao_retrospectiva.csv"

ml = pd.read_csv(arquivo_ml)
estatistico = pd.read_csv(arquivo_estatistico)

# Padroniza as colunas usadas na comparação
ml["ano"] = ml["ano_semana"]

ml["possivel_anomalia"] = (
    ml["possivel_anomalia"].astype(bool)
)

estatistico["possivel_alerta"] = (
    estatistico["possivel_alerta"].astype(bool)
)

comparacao = ml.merge(
    estatistico[
        ["ano", "semana", "possivel_alerta"]
    ],
    on=["ano", "semana"],
    how="inner"
)

# Identifica os resultados de cada método
comparacao["resultado_comparacao"] = comparacao.apply(
    lambda linha: (
        "Ambos sinalizaram"
        if linha["possivel_anomalia"] and linha["possivel_alerta"]
        else "Somente Isolation Forest"
        if linha["possivel_anomalia"]
        else "Somente método estatístico"
        if linha["possivel_alerta"]
        else "Nenhum sinalizou"
    ),
    axis=1
)

print("Resumo da comparação:")
print(
    comparacao["resultado_comparacao"]
    .value_counts()
    .to_string()
)

print("\nSemanas sinalizadas pelos dois métodos:")
print(
    comparacao[
        comparacao["resultado_comparacao"] == "Ambos sinalizaram"
    ][
        ["ano", "semana", "quantidade"]
    ].to_string(index=False)
)

comparacao.to_csv(
    "dados_processados/comparacao_modelos.csv",
    index=False
)

print("\nArquivo salvo: dados_processados/comparacao_modelos.csv")
