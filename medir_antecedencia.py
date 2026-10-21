
import pandas as pd

alertas = pd.read_csv(
    "dados_processados/comparacao_temporal_estatistico.csv"
)

# Marcos provisórios de crescimento para investigação
marcos = {
    2022: 5,
    2023: 5
}

for ano, semana_marco in marcos.items():
    dados_ano = alertas[
        alertas["ano"] == ano
    ].copy()

    sinalizados = dados_ano[
        dados_ano["possivel_anomalia"]
        | dados_ano["possivel_alerta"]
    ]

    anteriores = sinalizados[
        sinalizados["semana"] < semana_marco
    ]

    durante = sinalizados[
        sinalizados["semana"] == semana_marco
    ]

    print(f"\nAno {ano}")
    print(f"Semana de referência: {semana_marco}")

    if not anteriores.empty:
        primeira = int(anteriores["semana"].min())
        antecedencia = semana_marco - primeira

        print(f"Primeiro alerta anterior: semana {primeira}")
        print(f"Distância até a referência: {antecedencia} semanas")
    elif not durante.empty:
        print("Primeiro alerta identificado na própria semana de referência.")
    else:
        posteriores = sinalizados[
            sinalizados["semana"] > semana_marco
        ]

        if not posteriores.empty:
            primeira = int(posteriores["semana"].min())
            print(f"Primeiro alerta posterior: semana {primeira}")
            print("O alerta ocorreu depois da referência.")
        else:
            print("Nenhum alerta identificado no ano.")

    print(
        "Alertas antes da referência:",
        len(anteriores)
    )
