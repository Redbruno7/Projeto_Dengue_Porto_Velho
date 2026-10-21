import pandas as pd
from sklearn.ensemble import IsolationForest

arquivo = "dados_processados/dados_modelo_anomalias.csv"
dados = pd.read_csv(arquivo)

variaveis = [
    "quantidade",
    "casos_semana_anterior",
    "media_4_semanas_anteriores",
    "media_8_semanas_anteriores",
    "diferenca_media_4_semanas"
]

resultados = []

for ano in range(2021, 2026):
    treino = dados[dados["ano_semana"] < ano].copy()
    teste = dados[dados["ano_semana"] == ano].copy()

    if treino.empty or teste.empty:
        continue

    modelo = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    modelo.fit(treino[variaveis])

    teste["resultado_modelo"] = modelo.predict(
        teste[variaveis]
    )

    teste["possivel_anomalia"] = (
        teste["resultado_modelo"] == -1
    )

    resultados.append(teste)

    print(
        f"Ano {ano}: "
        f"{len(treino)} semanas para treino, "
        f"{len(teste)} semanas avaliadas, "
        f"{int(teste['possivel_anomalia'].sum())} possíveis anomalias"
    )

if resultados:
    avaliacao = pd.concat(resultados, ignore_index=True)

    avaliacao.to_csv(
        "dados_processados/isolation_forest_temporal.csv",
        index=False
    )

    print("\nResumo por ano:")
    print(
        avaliacao.groupby("ano_semana").agg(
            semanas_avaliadas=("semana", "count"),
            possiveis_anomalias=("possivel_anomalia", "sum")
        ).to_string()
    )

    print(
        "\nArquivo salvo: "
        "dados_processados/isolation_forest_temporal.csv"
    )
