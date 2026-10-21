import os
import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

# Caminhos dos arquivos
arquivo_csv = "dados_processados/casos_dengue_porto_velho.csv"
pasta_graficos = "graficos"

os.makedirs(pasta_graficos, exist_ok=True)

# Carrega os dados
dados = pd.read_csv(arquivo_csv)
dados["DT_SIN_PRI"] = pd.to_datetime(
    dados["DT_SIN_PRI"], errors="coerce"
)

# Extrai o ano de início dos sintomas
dados["ano_sintomas"] = dados["DT_SIN_PRI"].dt.year

# Seleciona o período de 2016 a 2025
periodo = dados[
    dados["ano_sintomas"].between(2016, 2025)
]

# Conta os registros por ano
casos_por_ano = (
    periodo.groupby("ano_sintomas")
    .size()
    .reindex(range(2016, 2026), fill_value=0)
)

print("Registros por ano:")
print(casos_por_ano.to_string())

# Cria o gráfico
plt.figure(figsize=(10, 6))
casos_por_ano.plot(kind="bar")
plt.title("Registros de dengue por ano - Porto Velho (2016–2025)")
plt.xlabel("Ano de início dos sintomas")
plt.ylabel("Quantidade de registros")
plt.xticks(rotation=0)
plt.tight_layout()

# Salva o gráfico
caminho_grafico = os.path.join(
    pasta_graficos, "casos_por_ano.png"
)
plt.savefig(caminho_grafico, dpi=300)
plt.close()

print(f"\nGráfico salvo em: {caminho_grafico}")


# Analisa os registros por semana epidemiológica
dados["SEM_PRI"] = pd.to_numeric(
    dados["SEM_PRI"], errors="coerce"
)

dados["ano_semana"] = dados["SEM_PRI"] // 100
dados["semana"] = dados["SEM_PRI"] % 100

# Seleciona o período de 2016 a 2025
dados_semanais = dados[
    dados["ano_semana"].between(2016, 2025)
    & dados["semana"].between(1, 53)
].copy()


# Conta os registros de cada semana epidemiológica
contagem_semanal = (
    dados_semanais
    .groupby(["ano_semana", "semana"])
    .size()
    .rename("quantidade")
)

# Inclui semanas sem registros, do início do ano até a
# última semana identificada nos dados de cada ano
combinacoes = []

for ano in range(2016, 2026):
    semanas_do_ano = dados_semanais.loc[
        dados_semanais["ano_semana"] == ano, "semana"
    ]

    if not semanas_do_ano.empty:
        ultima_semana = int(semanas_do_ano.max())

        for semana in range(1, ultima_semana + 1):
            combinacoes.append((ano, semana))

indice_completo = pd.MultiIndex.from_tuples(
    combinacoes,
    names=["ano_semana", "semana"]
)


# Conta os registros por ano e semana epidemiológica
casos_semanais = (
    dados_semanais
    .groupby(["ano_semana", "semana"])
    .size()
    .reset_index(name="quantidade")
)


# Cria o calendário até a última semana encontrada em cada ano
combinacoes = []

for ano in range(2016, 2026):
    semanas_do_ano = dados_semanais.loc[
        dados_semanais["ano_semana"] == ano,
        "semana"
    ]

    if not semanas_do_ano.empty:
        ultima_semana = int(semanas_do_ano.max())

        for semana in range(1, ultima_semana + 1):
            combinacoes.append((ano, semana))

calendario = pd.MultiIndex.from_tuples(
    combinacoes,
    names=["ano_semana", "semana"]
)

casos_semanais = (
    dados_semanais
    .groupby(["ano_semana", "semana"])
    .size()
    .rename("quantidade")
    .reindex(calendario, fill_value=0)
    .reset_index()
)

# Salva a tabela semanal completa
casos_semanais.to_csv(
    "dados_processados/casos_por_semana.csv",
    index=False
)

# Gera o gráfico semanal
plt.figure(figsize=(12, 6))

for ano, grupo in casos_semanais.groupby("ano_semana"):
    plt.plot(
        grupo["semana"],
        grupo["quantidade"],
        label=str(int(ano))
    )

plt.title("Registros de dengue por semana epidemiológica")
plt.xlabel("Semana epidemiológica")
plt.ylabel("Quantidade de registros")
plt.legend(title="Ano", ncol=2)
plt.tight_layout()

plt.savefig(
    os.path.join(pasta_graficos, "casos_por_semana.png"),
    dpi=300
)
plt.close()

# Exibe as dez semanas com mais registros
print("\n10 semanas com mais registros:")

top_semanas = casos_semanais.sort_values(
    by="quantidade",
    ascending=False
).head(10)

print(top_semanas.to_string(index=False))

top_semanas.to_csv(
    "dados_processados/top_10_semanas.csv",
    index=False
)

# Estatísticas da distribuição semanal
print("\nEstatísticas semanais:")
print(f"Média: {casos_semanais['quantidade'].mean():.2f}")
print(f"Mediana: {casos_semanais['quantidade'].median():.2f}")
print(f"Máximo: {casos_semanais['quantidade'].max()}")
print(f"Mínimo: {casos_semanais['quantidade'].min()}")

print("\nArquivos atualizados:")
print("Gráfico: graficos/casos_por_semana.png")
print("Tabela: dados_processados/casos_por_semana.csv")
print("Maiores semanas: dados_processados/top_10_semanas.csv")

# Identificação inicial de semanas com valores elevados

media_semanal = casos_semanais["quantidade"].mean()
desvio_padrao = casos_semanais["quantidade"].std()

limite_alerta = media_semanal + (2 * desvio_padrao)

casos_semanais["possivel_alerta"] = (
    casos_semanais["quantidade"] > limite_alerta
)

semanas_alerta = casos_semanais[
    casos_semanais["possivel_alerta"]
].copy()

print("\nAnálise inicial de possíveis alertas")
print(f"Média semanal: {media_semanal:.2f}")
print(f"Desvio-padrão: {desvio_padrao:.2f}")
print(f"Limite estatístico: {limite_alerta:.2f}")

print("\nSemanas acima do limite:")
print(
    semanas_alerta.sort_values(
        by="quantidade",
        ascending=False
    ).to_string(index=False)
)

semanas_alerta.to_csv(
    "dados_processados/semanas_com_alerta.csv",
    index=False
)

print(
    "\nArquivo salvo: "
    "dados_processados/semanas_com_alerta.csv"
)

# Compara cada ano com os demais anos da mesma semana epidemiológica
resultados = []

for _, linha in casos_semanais.iterrows():
    ano = int(linha["ano_semana"])
    semana = int(linha["semana"])
    quantidade = int(linha["quantidade"])

    historico = casos_semanais[
        (casos_semanais["semana"] == semana)
        & (casos_semanais["ano_semana"] != ano)
    ]["quantidade"]

    media_historica = historico.mean()
    desvio_historico = historico.std()
    anos_comparados = len(historico)

    if pd.isna(desvio_historico) or desvio_historico == 0:
        escore_z = None
    else:
        escore_z = (
            quantidade - media_historica
        ) / desvio_historico

    resultados.append({
        "ano_semana": ano,
        "semana": semana,
        "quantidade": quantidade,
        "media_historica": media_historica,
        "desvio_historico": desvio_historico,
        "anos_comparados": anos_comparados,
        "escore_z": escore_z
    })

comparacao = pd.DataFrame(resultados)

comparacao["possivel_anomalia"] = (
    comparacao["escore_z"] >= 2
)

comparacao.to_csv(
    "dados_processados/comparacao_historica_semanal.csv",
    index=False
)

print("\n15 semanas com maior escore Z:")

print(
    comparacao.sort_values(
        by="escore_z",
        ascending=False
    )[
        [
            "ano_semana",
            "semana",
            "quantidade",
            "media_historica",
            "desvio_historico",
            "escore_z",
            "possivel_anomalia"
        ]
    ].head(15).round(2).to_string(index=False)
)

print("\nTotal de semanas com escore Z >= 2:")
print(int(comparacao["possivel_anomalia"].sum()))

print(
    "\nArquivo salvo: "
    "dados_processados/comparacao_historica_semanal.csv"
)

# Filtra possíveis anomalias com histórico suficiente
anomalias_filtradas = comparacao[
    (comparacao["anos_comparados"] >= 5)
    & (comparacao["escore_z"] >= 2)
].copy()

anomalias_filtradas = anomalias_filtradas.sort_values(
    by="escore_z",
    ascending=False
)

print("\nPossíveis anomalias com pelo menos 5 anos de histórico:")

print(
    anomalias_filtradas[
        [
            "ano_semana",
            "semana",
            "quantidade",
            "media_historica",
            "desvio_historico",
            "escore_z"
        ]
    ].head(20).round(2).to_string(index=False)
)

print(
    "\nTotal após o filtro:",
    len(anomalias_filtradas)
)

anomalias_filtradas.to_csv(
    "dados_processados/anomalias_filtradas.csv",
    index=False
)

print(
    "Arquivo salvo: dados_processados/anomalias_filtradas.csv"
)

# Gráfico de registros semanais e referência histórica
plt.figure(figsize=(14, 6))

for ano, grupo in comparacao.groupby("ano_semana"):
    plt.plot(
        grupo["semana"],
        grupo["quantidade"],
        label=str(ano),
        alpha=0.65
    )

plt.title("Registros semanais de dengue por ano")
plt.xlabel("Semana epidemiológica")
plt.ylabel("Quantidade de registros")
plt.legend(title="Ano", ncol=2)
plt.tight_layout()

plt.savefig(
    os.path.join(pasta_graficos, "comparacao_semanal_anos.png"),
    dpi=300
)

plt.close()

print(
    "\nGráfico salvo: "
    "graficos/comparacao_semanal_anos.png"
)

# Análise retrospectiva usando apenas anos anteriores
resultados_historicos = []

for _, linha in casos_semanais.iterrows():
    ano = int(linha["ano_semana"])
    semana = int(linha["semana"])
    quantidade = int(linha["quantidade"])

    historico = casos_semanais[
        (casos_semanais["semana"] == semana)
        & (casos_semanais["ano_semana"] < ano)
    ]["quantidade"]

    if len(historico) < 3:
        continue

    media_historica = historico.mean()
    desvio_historico = historico.std()

    if pd.isna(desvio_historico) or desvio_historico == 0:
        escore_z = None
    else:
        escore_z = (
            quantidade - media_historica
        ) / desvio_historico

    resultados_historicos.append({
        "ano_semana": ano,
        "semana": semana,
        "quantidade": quantidade,
        "anos_comparados": len(historico),
        "media_historica": media_historica,
        "desvio_historico": desvio_historico,
        "escore_z": escore_z
    })

alertas_historicos = pd.DataFrame(resultados_historicos)

alertas_historicos["possivel_alerta"] = (
    alertas_historicos["escore_z"] >= 2
)

alertas_historicos.to_csv(
    "dados_processados/alertas_historico_anterior.csv",
    index=False
)

print("\nPossíveis alertas usando somente anos anteriores:")

print(
    alertas_historicos[
        alertas_historicos["possivel_alerta"]
    ].sort_values(
        by="escore_z",
        ascending=False
    )[
        [
            "ano_semana",
            "semana",
            "quantidade",
            "anos_comparados",
            "media_historica",
            "escore_z"
        ]
    ].head(20).round(2).to_string(index=False)
)

print(
    "\nTotal de possíveis alertas:",
    int(alertas_historicos["possivel_alerta"].sum())
)

print(
    "Arquivo salvo: "
    "dados_processados/alertas_historico_anterior.csv"
)

# Resumo dos possíveis alertas por ano
resumo_alertas = (
    alertas_historicos[
        alertas_historicos["possivel_alerta"]
    ]
    .groupby("ano_semana")
    .size()
    .reset_index(name="quantidade_alertas")
)

print("\nQuantidade de possíveis alertas por ano:")
print(resumo_alertas.to_string(index=False))

resumo_alertas.to_csv(
    "dados_processados/resumo_alertas_por_ano.csv",
    index=False
)

print(
    "\nArquivo salvo: "
    "dados_processados/resumo_alertas_por_ano.csv"
)

# Verifica a quantidade de semanas por ano na tabela semanal

semanas_por_ano = (
    casos_semanais
    .groupby("ano_semana")["semana"]
    .nunique()
    .reset_index(name="total_semanas")
)

print("\nQuantidade de semanas por ano:")
print(semanas_por_ano.to_string(index=False))

print("\nSemanas 53 por ano:")
print(
    casos_semanais[
        casos_semanais["semana"] == 53
    ][["ano_semana", "semana", "quantidade"]]
    .to_string(index=False)
)

# Verifica as semanas epidemiológicas existentes nos dados originais

semanas_originais = dados.copy()

semanas_originais["SEM_PRI"] = pd.to_numeric(
    semanas_originais["SEM_PRI"],
    errors="coerce"
)

semanas_originais["ano_semana"] = (
    semanas_originais["SEM_PRI"] // 100
)

semanas_originais["semana"] = (
    semanas_originais["SEM_PRI"] % 100
)

semanas_originais = semanas_originais[
    semanas_originais["ano_semana"].between(2016, 2025)
    & semanas_originais["semana"].between(1, 53)
]

print("\nMaior semana epidemiológica encontrada em cada ano:")

print(
    semanas_originais.groupby("ano_semana")["semana"]
    .max()
    .reset_index(name="ultima_semana_encontrada")
    .to_string(index=False)
)

print("\nQuantidade de registros na semana 53 da base original:")

print(
    semanas_originais[
        semanas_originais["semana"] == 53
    ].groupby("ano_semana")
    .size()
    .reindex(range(2016, 2026), fill_value=0)
    .to_string()
)


# Simulação retrospectiva de alertas a partir de 2021

resultados_simulacao = []

for ano in range(2021, 2026):
    dados_ano = casos_semanais[
        casos_semanais["ano_semana"] == ano
    ]

    for _, linha in dados_ano.iterrows():
        semana = int(linha["semana"])
        quantidade = int(linha["quantidade"])

        historico = casos_semanais[
            (casos_semanais["semana"] == semana)
            & (casos_semanais["ano_semana"] < ano)
        ]["quantidade"]

        if len(historico) < 5:
            continue

        media_historica = historico.mean()

        limite_alerta = max(
            media_historica * 2,
            media_historica + 5
        )

        possivel_alerta = quantidade > limite_alerta

        resultados_simulacao.append({
            "ano": ano,
            "semana": semana,
            "quantidade": quantidade,
            "anos_historicos": len(historico),
            "media_historica": round(media_historica, 2),
            "limite_alerta": round(limite_alerta, 2),
            "possivel_alerta": possivel_alerta
        })

simulacao = pd.DataFrame(resultados_simulacao)

simulacao.to_csv(
    "dados_processados/simulacao_retrospectiva.csv",
    index=False
)

print("\nResumo da simulação retrospectiva:")

print(
    simulacao.groupby("ano").agg(
        semanas_avaliadas=("semana", "count"),
        possiveis_alertas=("possivel_alerta", "sum")
    ).to_string()
)

print(
    "\nArquivo salvo: "
    "dados_processados/simulacao_retrospectiva.csv"
)


# Gráfico dos possíveis alertas por ano

resumo_simulacao = (
    simulacao.groupby("ano")
    .agg(
        semanas_avaliadas=("semana", "count"),
        possiveis_alertas=("possivel_alerta", "sum")
    )
    .reset_index()
)

plt.figure(figsize=(10, 6))

plt.bar(
    resumo_simulacao["ano"].astype(str),
    resumo_simulacao["possiveis_alertas"]
)

plt.title("Possíveis alertas identificados por ano")
plt.xlabel("Ano")
plt.ylabel("Quantidade de possíveis alertas")
plt.tight_layout()

caminho_grafico = os.path.join(
    pasta_graficos,
    "alertas_por_ano.png"
)

plt.savefig(caminho_grafico, dpi=300)
plt.close()

print(f"\nGráfico de alertas salvo em: {caminho_grafico}")


# Detalhamento dos possíveis alertas por ano

alertas_detalhados = simulacao[
    simulacao["possivel_alerta"]
].copy()

alertas_detalhados = alertas_detalhados.sort_values(
    by=["ano", "quantidade"],
    ascending=[True, False]
)

print("\nDetalhamento dos possíveis alertas:")

for ano, grupo in alertas_detalhados.groupby("ano"):
    print(f"\nAno: {ano}")
    print(
        grupo[
            [
                "semana",
                "quantidade",
                "media_historica",
                "limite_alerta"
            ]
        ].to_string(index=False)
    )

alertas_detalhados.to_csv(
    "dados_processados/alertas_detalhados.csv",
    index=False
)

print(
    "\nArquivo salvo: "
    "dados_processados/alertas_detalhados.csv"
)


# Compara os registros com o limite histórico de alerta

for ano in [2022, 2023, 2024]:
    dados_grafico = simulacao[
        simulacao["ano"] == ano
    ].sort_values("semana")

    plt.figure(figsize=(12, 6))

    plt.plot(
        dados_grafico["semana"],
        dados_grafico["quantidade"],
        label="Registros observados",
        marker="o",
        markersize=3
    )

    plt.plot(
        dados_grafico["semana"],
        dados_grafico["limite_alerta"],
        label="Limite de alerta",
        linestyle="--"
    )

    plt.title(
        f"Registros semanais e limite histórico - {ano}"
    )
    plt.xlabel("Semana epidemiológica")
    plt.ylabel("Quantidade de registros")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    caminho = os.path.join(
        pasta_graficos,
        f"comparacao_alertas_{ano}.png"
    )

    plt.savefig(caminho, dpi=300)
    plt.close()

    print(f"Gráfico salvo: {caminho}")
