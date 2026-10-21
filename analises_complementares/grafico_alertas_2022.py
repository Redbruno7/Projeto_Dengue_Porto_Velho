
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Carrega os dados semanais
casos = pd.read_csv(
    "dados_processados/casos_por_semana.csv"
)

# Carrega os resultados dos modelos
ml = pd.read_csv(
    "dados_processados/isolation_forest_temporal.csv"
)

estatistico = pd.read_csv(
    "dados_processados/simulacao_retrospectiva.csv"
)

# Seleciona o ano de 2022
casos = casos[casos["ano_semana"] == 2022].copy()

ml = ml[ml["ano_semana"] == 2022].copy()

estatistico = estatistico[
    estatistico["ano"] == 2022
].copy()

# Junta os resultados pela semana
grafico = casos.merge(
    ml[["semana", "possivel_anomalia"]],
    on="semana",
    how="left"
)

grafico = grafico.merge(
    estatistico[["semana", "possivel_alerta"]],
    on="semana",
    how="left"
)

grafico["possivel_anomalia"] = (
    grafico["possivel_anomalia"].fillna(False).astype(bool)
)

grafico["possivel_alerta"] = (
    grafico["possivel_alerta"].fillna(False).astype(bool)
)

# Cria o gráfico
plt.figure(figsize=(14, 6))

plt.plot(
    grafico["semana"],
    grafico["quantidade"],
    label="Casos semanais",
    marker="o",
    linewidth=1.8
)

# Alertas estatísticos
plt.scatter(
    grafico.loc[
        grafico["possivel_alerta"], "semana"
    ] - 0.15,
    grafico.loc[
        grafico["possivel_alerta"], "quantidade"
    ],
    label="Alerta estatístico",
    marker="^",
    s=90,
    zorder=3
)

# Anomalias do Isolation Forest
plt.scatter(
    grafico.loc[
        grafico["possivel_anomalia"], "semana"
    ] + 0.15,
    grafico.loc[
        grafico["possivel_anomalia"], "quantidade"
    ],
    label="Isolation Forest",
    marker="s",
    s=65,
    zorder=4
)

plt.title("Casos semanais e alertas de anomalias — Porto Velho, 2022")
plt.xlabel("Semana epidemiológica")
plt.ylabel("Quantidade de casos")
plt.xticks(range(1, 53, 2))
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig(
    "graficos/alertas_modelos_2022.png",
    dpi=150
)

plt.close()

print("Gráfico salvo em graficos/alertas_modelos_2022.png")
