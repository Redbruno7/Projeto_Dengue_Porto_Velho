
import zipfile
from pathlib import Path
from collections import Counter

import pandas as pd

with zipfile.ZipFile("dados_brutos/DENGBR24.csv.zip") as arquivo_zip:
    nome_csv = next(
        nome for nome in arquivo_zip.namelist()
        if nome.lower().endswith(".csv")
    )

    with arquivo_zip.open(nome_csv) as arquivo:
        dados = pd.read_csv(
            arquivo,
            sep=",",
            encoding="latin1",
            dtype=str,
            nrows=100_000
        )

dados.columns = dados.columns.str.strip().str.upper()

print("Valores de SG_UF:")
print(dados["SG_UF"].value_counts(dropna=False).head(20))

print("\nValores de SG_UF_NOT:")
print(dados["SG_UF_NOT"].value_counts(dropna=False).head(20))

print("\nValores de ID_MN_RESI:")
print(dados["ID_MN_RESI"].value_counts(dropna=False).head(20))

print("\nValores de ID_MUNICIP:")
print(dados["ID_MUNICIP"].value_counts(dropna=False).head(20))