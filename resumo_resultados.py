
import pandas as pd

# Carrega os dados
casos = pd.read_csv(
    "dados_processados/casos_por_semana.csv"
)

ml = pd.read_csv(
    "dados_processados/isolation_forest_temporal.csv"
)

estatistico = pd.read_csv(
    "dados_processados/simulacao_retrospectiva.csv"
)

comparacao = pd.read_csv(
    "dados_processados/comparacao_temporal_estatistico.csv"
)

# Total de casos por ano
totais_casos = (
    casos.groupby("ano_semana")["quantidade"]
    .sum()
    .rename("total_casos")
)

# Quantidade de semanas sinalizadas pelo Isolation Forest
totais_ml = (
    ml[ml["possivel_anomalia"]]
    .groupby("ano_semana")
    .size()
    .rename("anomalias_isolation_forest")
)

# Quantidade de alertas estatísticos
totais_estatisticos = (
    estatistico[estatistico["possivel_alerta"]]
    .groupby("ano")["semana"]
    .count()
    .rename("alertas_estatisticos")
)

# Semanas sinalizadas por ambos os métodos
ambos = (
    comparacao[
        comparacao["resultado_comparacao"] == "Ambos sinalizaram"
    ]
    .groupby("ano")
    .size()
    .rename("alertas_em_comum")
)

# Consolida os resultados
resumo = pd.concat(
    [totais_casos, totais_ml, totais_estatisticos, ambos],
    axis=1
).fillna(0)

resumo.index.name = "ano"
resumo = resumo.reset_index()

colunas_contagem = [
    "total_casos",
    "anomalias_isolation_forest",
    "alertas_estatisticos",
    "alertas_em_comum"
]

resumo[colunas_contagem] = (
    resumo[colunas_contagem].astype(int)
)

resumo.to_csv(
    "dados_processados/resumo_resultados.csv",
    index=False
)

print("Resumo consolidado por ano:")
print(resumo.to_string(index=False))

print(
    "\nArquivo salvo: "
    "dados_processados/resumo_resultados.csv"
)
