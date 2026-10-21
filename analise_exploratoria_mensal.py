
from pathlib import Path

import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

arquivo = Path("dados_processados/casos_mensais_risco.csv")
pasta_graficos = Path("graficos")
pasta_graficos.mkdir(parents=True, exist_ok=True)

dados = pd.read_csv(arquivo)

# Gráfico 1: quantidade de casos por mês
plt.figure(figsize=(12, 5))
plt.plot(
    dados["mes"],
    dados["quantidade_casos"],
    marker="o",
    markersize=3
)

plt.title("Casos mensais de dengue em Porto Velho (2016–2025)")
plt.xlabel("Mês")
plt.ylabel("Quantidade de casos")
plt.xticks(rotation=90)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    pasta_graficos / "casos_mensais_dengue.png",
    dpi=150
)
plt.close()

# Gráfico 2: distribuição das classes de risco
ordem = ["Baixo", "Médio", "Alto"]
distribuicao = (
    dados["risco"]
    .value_counts()
    .reindex(ordem, fill_value=0)
)

plt.figure(figsize=(7, 5))
distribuicao.plot(kind="bar")

plt.title("Distribuição das classes de risco")
plt.xlabel("Classe de risco")
plt.ylabel("Quantidade de meses")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(
    pasta_graficos / "distribuicao_classes_risco.png",
    dpi=150
)
plt.close()

print("Análise exploratória concluída.")
print("\nEstatísticas dos casos mensais:")
print(dados["quantidade_casos"].describe().round(2))
print("\nDistribuição das classes:")
print(distribuicao.to_string())
print("\nGráficos salvos na pasta graficos.")
