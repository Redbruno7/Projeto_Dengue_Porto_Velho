
from pathlib import Path

import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    confusion_matrix
)

arquivo = Path("dados_processados/casos_mensais_risco.csv")
dados = pd.read_csv(arquivo)

# Criar variáveis com informações disponíveis antes do mês avaliado
dados["mes_numero"] = pd.to_datetime(
    dados["mes"]
).dt.month

dados["casos_mes_anterior"] = (
    dados["quantidade_casos"].shift(1)
)

dados["casos_dois_meses_antes"] = (
    dados["quantidade_casos"].shift(2)
)

dados["casos_tres_meses_antes"] = (
    dados["quantidade_casos"].shift(3)
)

dados = dados.dropna().copy()

variaveis = [
    "mes_numero",
    "casos_mes_anterior",
    "casos_dois_meses_antes",
    "casos_tres_meses_antes"
]

X = dados[variaveis]
y = dados["risco"]

# Separação cronológica: 70% para treino e 30% para teste
ponto_corte = int(len(dados) * 0.7)

X_treino = X.iloc[:ponto_corte]
X_teste = X.iloc[ponto_corte:]

y_treino = y.iloc[:ponto_corte]
y_teste = y.iloc[ponto_corte:]

modelos = {
    "Árvore de Decisão": DecisionTreeClassifier(
        max_depth=4,
        random_state=42
    ),
    "KNN": make_pipeline(
        StandardScaler(),
        KNeighborsClassifier(n_neighbors=5)
    ),
    "SVM": make_pipeline(
        StandardScaler(),
        SVC(kernel="rbf")
    )
}

resultados = []

for nome, modelo in modelos.items():
    modelo.fit(X_treino, y_treino)
    previsoes = modelo.predict(X_teste)

    acuracia = accuracy_score(y_teste, previsoes)
    precisao = precision_score(
        y_teste,
        previsoes,
        average="macro",
        zero_division=0
    )
    revocacao = recall_score(
        y_teste,
        previsoes,
        average="macro",
        zero_division=0
    )

    resultados.append({
        "Modelo": nome,
        "Acurácia": round(acuracia, 4),
        "Precisão macro": round(precisao, 4),
        "Recall macro": round(revocacao, 4)
    })

    print(f"\nModelo: {nome}")
    print("Matriz de confusão:")
    print(confusion_matrix(
        y_teste,
        previsoes,
        labels=["Baixo", "Médio", "Alto"]
    ))


tabela_resultados = pd.DataFrame(resultados)

print("\n=== Comparação dos modelos ===")
print(tabela_resultados.to_string(index=False))

arquivo_resultados = Path(
    "dados_processados/comparacao_modelos.csv"
)

arquivo_resultados.parent.mkdir(
    parents=True,
    exist_ok=True
)

tabela_resultados.to_csv(
    arquivo_resultados,
    index=False
)

print("\nMeses usados para treinamento:", len(X_treino))
print("Meses usados para teste:", len(X_teste))
print(f"Resultados salvos em: {arquivo_resultados}")
