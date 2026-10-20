import csv
import zipfile
from pathlib import Path
import pandas as pd


# ==========================================
# 1. CONFIGURAÇÕES DO PROJETO
# ==========================================

PASTA_PROJETO = Path(__file__).resolve().parent
PASTA_DADOS = PASTA_PROJETO / "dados_brutos"
PASTA_PROCESSADOS = PASTA_PROJETO / "dados_processados"

# Código municipal de Porto Velho no padrão de 6 dígitos
CODIGO_MUNICIPIO = "110020"
UF_ALVO = "11"

# Arquivos anuais: 2016 a 2025
ARQUIVOS = sorted(PASTA_DADOS.glob("DENGBR*.csv.zip"))
TAMANHO_LOTE = 100_000

COLUNAS_DESEJADAS = [
    "DT_SIN_PRI",
    "DT_NOTIFIC",
    "NU_ANO",
    "SEM_PRI",
    "SEM_NOT",
    "SG_UF",
    "ID_MN_RESI",
    "CLASSI_FIN",
    "NDUPLIC_N",
]


# ==========================================
# 2. PREPARAR AS PASTAS
# ==========================================

PASTA_PROCESSADOS.mkdir(parents=True, exist_ok=True)

if not ARQUIVOS:
    raise FileNotFoundError(
        "Nenhum arquivo DENGBR*.csv.zip foi encontrado "
        "na pasta dados_brutos."
    )

print("=" * 55)
print("PROJETO DE IA - RISCO DE DENGUE")
print("Município: Porto Velho - RO")
print("=" * 55)
print(f"\nArquivos encontrados: {len(ARQUIVOS)}")


# ==========================================
# 3. LER E FILTRAR OS ARQUIVOS
# ==========================================

partes_filtradas = []
resumo = []

for caminho_zip in ARQUIVOS:
    print(f"\nProcessando: {caminho_zip.name}")

    try:
        with zipfile.ZipFile(caminho_zip, "r") as arquivo_zip:
            nomes_csv = [
                nome for nome in arquivo_zip.namelist()
                if nome.lower().endswith(".csv")
            ]

            if not nomes_csv:
                raise ValueError(
                    "O arquivo ZIP não contém nenhum CSV."
                )

            nome_csv = nomes_csv[0]

            # Detectar o separador do arquivo
            with arquivo_zip.open(nome_csv) as arquivo:
                amostra = arquivo.read(65536).decode(
                    "latin1", errors="replace"
                )

            try:
                delimitador = csv.Sniffer().sniff(
                    amostra,
                    delimiters=";,\t|"
                ).delimiter
            except csv.Error:
                delimitador = ";"

            print(f"Separador detectado: {repr(delimitador)}")

            total_lido = 0
            total_municipio = 0
            total_confirmado = 0
            total_excluido_duplicidade = 0

            with arquivo_zip.open(nome_csv) as arquivo:
                import io

                arquivo_texto = io.TextIOWrapper(
                    arquivo,
                    encoding="latin1",
                    errors="replace",
                    newline=""
                )

                lotes = pd.read_csv(
                    arquivo_texto,
                    sep=delimitador,
                    dtype=str,
                    chunksize=TAMANHO_LOTE,
                    keep_default_na=False,
                    on_bad_lines="warn"
                )

                for lote in lotes:
                    total_lido += len(lote)

                    # Padronizar nomes das colunas
                    lote.columns = (
                        lote.columns.str.replace("\ufeff", "", regex=False)
                        .str.strip()
                        .str.upper()
                    )

                    obrigatorias = {
                        "SG_UF",
                        "ID_MN_RESI",
                        "CLASSI_FIN",
                        "DT_SIN_PRI",
                    }

                    faltantes = obrigatorias - set(lote.columns)

                    if faltantes:
                        raise ValueError(
                            "Colunas obrigatórias não encontradas: "
                            + ", ".join(sorted(faltantes))
                        )

                    # Normalizar os campos utilizados no filtro
                    uf = (
                        lote["SG_UF"]
                        .fillna("")
                        .astype(str)
                        .str.strip()
                        .str.replace(r"\.0$", "", regex=True)
                    )

                    municipio = (
                        lote["ID_MN_RESI"]
                        .fillna("")
                        .astype(str)
                        .str.strip()
                        .str.replace(r"\.0$", "", regex=True)
                    )

                    classificacao = lote["CLASSI_FIN"].fillna(
                        "").astype(str).str.strip()

                    # Selecionar residentes de Porto Velho
                    mascara_municipio = (
                        (uf == UF_ALVO)
                        & (municipio == CODIGO_MUNICIPIO)
                    )

                    residentes = lote.loc[mascara_municipio].copy()

                    total_municipio += len(residentes)

                    # Manter somente casos confirmados
                    classificacao = residentes["CLASSI_FIN"].str.strip()

                    confirmados = residentes.loc[
                        classificacao.isin(["1", "2", "3", "4", "10", "11", "12"])
                    ].copy()

                    total_confirmado += len(confirmados)

                    # Excluir registros marcados como duplicidade
                    if "NDUPLIC_N" in confirmados.columns:
                        duplicados = (
                            confirmados["NDUPLIC_N"]
                            .str.strip() == "2"
                        )

                        total_excluido_duplicidade += int(
                            duplicados.sum()
                        )

                        confirmados = confirmados.loc[
                            ~duplicados
                        ].copy()

                    # Selecionar apenas as colunas relevantes
                    colunas_presentes = [
                        coluna for coluna in COLUNAS_DESEJADAS
                        if coluna in confirmados.columns
                    ]

                    partes_filtradas.append(
                        confirmados[colunas_presentes].copy()
                    )

            total_final = sum(
                len(parte) for parte in partes_filtradas
            )

            resumo.append({
                "arquivo": caminho_zip.name,
                "registros_lidos": total_lido,
                "residentes_porto_velho": total_municipio,
                "confirmados_antes_duplicidade": total_confirmado,
                "duplicidades_excluidas": total_excluido_duplicidade,
            })

            print(f"Registros lidos: {total_lido:,}")
            print(f"Residentes em Porto Velho: {total_municipio:,}")
            print(f"Casos confirmados: {total_confirmado:,}")
            print("Duplicidades excluídas: "f"{total_excluido_duplicidade:,}")

    except Exception as erro:
        raise RuntimeError(
            f"Falha ao processar {caminho_zip.name}: {erro}"
        ) from erro


# ==========================================
# 4. JUNTAR OS REGISTROS
# ==========================================

if not partes_filtradas or not any(
    not parte.empty for parte in partes_filtradas
):
    raise ValueError(
        "Nenhum registro foi selecionado. "
        "Confira os nomes das colunas e o código municipal."
    )

dados = pd.concat(
    partes_filtradas,
    ignore_index=True
)

# Garantir que todas as colunas previstas existam
for coluna in COLUNAS_DESEJADAS:
    if coluna not in dados.columns:
        dados[coluna] = ""

dados = dados[COLUNAS_DESEJADAS]

# Remover duplicatas exatas entre os registros selecionados
quantidade_antes = len(dados)
dados = dados.drop_duplicates().reset_index(drop=True)
duplicatas_exatas = quantidade_antes - len(dados)

# Salvar o banco de dados
caminho_saida = (PASTA_PROCESSADOS / "casos_dengue_porto_velho.csv")

dados.to_csv(
    caminho_saida,
    index=False,
    encoding="utf-8-sig"
)


# ==========================================
# 5. SALVAR O RESUMO DA COLETA
# ==========================================

df_resumo = pd.DataFrame(resumo)
caminho_resumo = (PASTA_PROCESSADOS / "resumo_coleta.csv")

df_resumo.to_csv(
    caminho_resumo,
    index=False,
    encoding="utf-8-sig"
)


# ==========================================
# 6. APRESENTAR OS RESULTADOS
# ==========================================

print("\n" + "=" * 55)
print("COLETA CONCLUÍDA")
print("=" * 55)
print(f"Registros no banco final: {len(dados):,}")
print(f"Duplicatas exatas removidas: {duplicatas_exatas:,}")
print(f"\nBanco de dados: {caminho_saida}")
print(f"Resumo da coleta: {caminho_resumo}")
print("\nPrimeiros registros:")
print(dados.head().to_string(index=False))
print("\nQuantidade de registros por ano de origem:")
print(df_resumo.to_string(index=False))
