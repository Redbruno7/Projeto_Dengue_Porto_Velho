import os
import pandas as pd
from sklearn.ensemble import IsolationForest

arquivo_entrada = "dados_processados/dados_modelo_anomalias.csv"
arquivo_saida = "dados_processados/resultado_isolation_forest.csv"

dados = pd.read_csv(arquivo_entrada)

variaveis = [
    "quantidade",
    "casos_semana_anterior",
    "media_4_semanas_anteriores",
    "media_8_semanas_anteriores",
    "diferenca_media_4_semanas"
]

X = dados[variaveis]

# Treina o modelo de detecção de anomalias
modelo = IsolationForest(
    contamination=0.05,
    random_state=42
)

dados["resultado_modelo"] = modelo.fit_predict(X)

# 1 = padrão comum; -1 = possível anomalia
dados["possivel_anomalia"] = (
    dados["resultado_modelo"] == -1
)

dados.to_csv(arquivo_saida, index=False)

print("Treinamento concluído.")
print("\nResumo dos resultados:")
print(
    dados["possivel_anomalia"]
    .value_counts()
    .rename(index={True: "Possível anomalia", False: "Padrão comum"})
    .to_string()
)

print("\nDez semanas mais recentes:")
print(
    dados[
        ["ano_semana", "semana", "quantidade", "possivel_anomalia"]
    ].tail(10).to_string(index=False)
)

print(f"\nArquivo salvo: {arquivo_saida}")


# Lista as semanas identificadas como possíveis anomalias

anomalias = dados[
    dados["possivel_anomalia"]
].copy()

anomalias = anomalias.sort_values(
    ["ano_semana", "semana"]
)

print("\nPossíveis anomalias por ano:")
print(
    anomalias.groupby("ano_semana").size().to_string()
)

print("\nDetalhes das possíveis anomalias:")
print(
    anomalias[
        [
            "ano_semana",
            "semana",
            "quantidade",
            "media_4_semanas_anteriores",
            "diferenca_media_4_semanas"
        ]
    ].to_string(index=False)
)

anomalias.to_csv(
    "dados_processados/anomalias_isolation_forest.csv",
    index=False
)

print(
    "\nArquivo salvo: "
    "dados_processados/anomalias_isolation_forest.csv"
)
