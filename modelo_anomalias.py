
import os
import pandas as pd

arquivo_csv = "dados_processados/casos_por_semana.csv"
pasta_dados = "dados_processados"

os.makedirs(pasta_dados, exist_ok=True)

dados = pd.read_csv(arquivo_csv)

dados = dados.sort_values(
    ["ano_semana", "semana"]
).reset_index(drop=True)

# Cria uma sequência contínua de semanas entre os anos
dados["casos_semana_anterior"] = (
    dados["quantidade"].shift(1)
)

dados["media_4_semanas_anteriores"] = (
    dados["quantidade"]
    .shift(1)
    .rolling(window=4, min_periods=4)
    .mean()
)

dados["media_8_semanas_anteriores"] = (
    dados["quantidade"]
    .shift(1)
    .rolling(window=8, min_periods=8)
    .mean()
)

dados["diferenca_media_4_semanas"] = (
    dados["quantidade"]
    - dados["media_4_semanas_anteriores"]
)

variaveis = [
    "quantidade",
    "casos_semana_anterior",
    "media_4_semanas_anteriores",
    "media_8_semanas_anteriores",
    "diferenca_media_4_semanas"
]

dados_modelo = dados.dropna(
    subset=variaveis
).copy()

print("\nDiagnóstico:")
print("Total de linhas:", len(dados))
print("Valores ausentes por variável:")
print(dados[variaveis].isna().sum())
print("Linhas descartadas:", len(dados) - len(dados_modelo))

caminho_saida = os.path.join(
    pasta_dados,
    "dados_modelo_anomalias.csv"
)

dados_modelo.to_csv(caminho_saida, index=False)

print("Preparação dos dados concluída.")
print(f"Semanas originais: {len(dados)}")
print(f"Semanas preparadas: {len(dados_modelo)}")

print("\nPrimeiras linhas:")
print(
    dados_modelo[
        ["ano_semana", "semana"] + variaveis
    ].head(10).to_string(index=False)
)

print(f"\nArquivo salvo: {caminho_saida}")
