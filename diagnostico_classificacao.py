
import zipfile
from pathlib import Path

import pandas as pd

PASTA_DADOS = Path("dados_brutos")
CODIGO_MUNICIPIO = "110020"
UF_ALVO = "11"

for caminho_zip in sorted(PASTA_DADOS.glob("DENGBR*.csv.zip")):
    print(f"\n{'=' * 45}")
    print(caminho_zip.name)

    with zipfile.ZipFile(caminho_zip, "r") as arquivo_zip:
        nome_csv = next(
            nome for nome in arquivo_zip.namelist()
            if nome.lower().endswith(".csv")
        )

        with arquivo_zip.open(nome_csv) as arquivo:
            lotes = pd.read_csv(
                arquivo,
                sep=",",
                encoding="latin1",
                dtype=str,
                chunksize=100_000,
                keep_default_na=False,
                low_memory=False
            )

            total_residentes = 0
            classificacoes = {}

            for lote in lotes:
                lote.columns = (
                    lote.columns.str.replace("\ufeff", "", regex=False)
                    .str.strip()
                    .str.upper()
                )

                uf = lote["SG_UF"].str.strip()
                municipio = (
                    lote["ID_MN_RESI"]
                    .str.strip()
                    .str.replace(r"\.0$", "", regex=True)
                )

                filtro = (
                    uf.eq(UF_ALVO)
                    & municipio.eq(CODIGO_MUNICIPIO)
                )

                residentes = lote.loc[filtro]
                total_residentes += len(residentes)

                contagem = (
                    residentes["CLASSI_FIN"]
                    .str.strip()
                    .replace("", "(vazio)")
                    .value_counts()
                )

                for codigo, quantidade in contagem.items():
                    classificacoes[codigo] = (
                        classificacoes.get(codigo, 0) + quantidade
                    )

    print("Residentes encontrados:", total_residentes)
    print("Valores de CLASSI_FIN:")

    for codigo, quantidade in sorted(classificacoes.items()):
        print(f"  {codigo}: {quantidade}")
