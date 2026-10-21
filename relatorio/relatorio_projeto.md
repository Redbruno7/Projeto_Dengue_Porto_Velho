# Uso da Inteligência Artificial para Auxílio à Detecção de Risco de Surto de Dengue em Porto Velho – RO

## 1. Introdução

A dengue é um problema de saúde pública no Brasil, especialmente em regiões que apresentam condições favoráveis à proliferação do mosquito *Aedes aegypti*. O acompanhamento dos casos registrados é importante para compreender a variação da doença ao longo do tempo e auxiliar na identificação de períodos que exigem maior atenção das autoridades de saúde.

Nesse contexto, a análise de dados históricos pode contribuir para a compreensão do comportamento da dengue em diferentes localidades. Técnicas de Inteligência Artificial, especialmente os algoritmos de classificação, permitem identificar padrões nos dados e associar os registros a categorias previamente definidas.

Este projeto utiliza dados do Sistema de Informação de Agravos de Notificação (SINAN) referentes ao município de Porto Velho, Rondônia, para organizar os registros de dengue por mês e classificá-los em três níveis de risco: baixo, médio e alto. Para isso, são treinados e avaliados diferentes modelos de classificação, cujos resultados são comparados por meio de métricas de desempenho.

A proposta busca demonstrar como técnicas de Inteligência Artificial podem ser aplicadas à análise de dados epidemiológicos, considerando as limitações dos registros disponíveis e dos critérios utilizados para definir as classes. O trabalho possui caráter acadêmico e exploratório, não substituindo as avaliações epidemiológicas realizadas pelos órgãos de saúde.

## 2. Objetivo

Desenvolver e avaliar modelos de Inteligência Artificial capazes de classificar o nível mensal de risco de dengue em Porto Velho, Rondônia, a partir de dados históricos do SINAN, comparando o desempenho de três algoritmos de classificação por meio de métricas de avaliação.

## 3. Metodologia

### 3.1 Coleta dos dados

Os dados utilizados neste projeto foram obtidos a partir dos arquivos de notificações de dengue do Sistema de Informação de Agravos de Notificação (SINAN), disponibilizados por meio do OpenDataSUS. Foram considerados registros referentes ao período de 2016 a 2025, abrangendo dez anos de informações.

Para delimitar o estudo ao município de Porto Velho, em Rondônia, foi aplicado um filtro utilizando o código municipal 110020 e o código da unidade federativa de Rondônia (11). Os arquivos foram processados por meio de um script desenvolvido em Python, que reuniu os registros selecionados em uma única base de dados, facilitando as etapas posteriores de preparação e análise.

Após a coleta e a filtragem, a base consolidada apresentou 4.082 registros para processamento. Esses dados constituíram a fonte inicial para a organização dos casos por mês e para a construção da base utilizada na classificação dos níveis de risco.

### 3.2 Preparação dos dados

Após a coleta, os registros passaram por uma etapa de filtragem e preparação utilizando Python e a biblioteca Pandas. Foram selecionados os registros de residentes de Porto Velho que atendiam aos critérios de classificação final definidos no script de coleta. O campo `NDUPLIC_N` também foi verificado, mas não resultou na exclusão de registros nos arquivos analisados. Após a consolidação dos dados, foram removidas 1.689 duplicatas exatas, ou seja, linhas que apresentavam valores idênticos em todas as colunas. Ao final desse processo, a base consolidada ficou com 4.082 registros.

Para construir a base mensal, a coluna `DT_SIN_PRI`, correspondente à data de início dos sintomas, foi convertida para o formato de data. Os registros que não apresentaram uma data válida foram desconsiderados nessa etapa. Em seguida, os casos foram agrupados por mês, contando-se os registros de cada período. Os meses sem registros entre o início e o fim da série foram incluídos com quantidade igual a zero, garantindo a continuidade da sequência mensal.

Para a classificação mensal, foram adotados limites didáticos de quantidade de casos: risco baixo para até 9 casos, risco médio para 10 a 30 casos e risco alto para mais de 30 casos. Esses critérios foram utilizados para estabelecer as classes do problema de classificação e não correspondem a níveis oficiais de alerta epidemiológico.

A base mensal resultante contém 120 meses, abrangendo o período de janeiro de 2016 a dezembro de 2025. Essa estrutura foi utilizada na análise exploratória e no treinamento dos modelos de classificação.

### 3.3 Análise exploratória

A análise exploratória foi realizada com o objetivo de observar a variação mensal dos casos de dengue ao longo do período estudado e verificar a distribuição dos níveis de risco definidos para a classificação. Para isso, foram utilizados gráficos produzidos com a biblioteca Matplotlib, a partir da base mensal preparada anteriormente.

O primeiro gráfico apresenta a quantidade de casos registrados em cada mês, permitindo visualizar as oscilações ao longo da série histórica e identificar períodos com maior ou menor número de registros. Essa visualização contribui para compreender a variação dos casos durante os dez anos analisados.

O segundo gráfico apresenta a distribuição dos meses entre as três classes de risco. Do total de 120 meses, 41 foram classificados como risco baixo, 41 como risco médio e 38 como risco alto. Essa distribuição indica que as classes possuem quantidades relativamente próximas de registros, aspecto relevante para a etapa de treinamento e avaliação dos classificadores.

Os gráficos utilizados nesta análise são apresentados na Figura 1, referente à quantidade mensal de casos, e na Figura 2, referente à distribuição das classes de risco.

### 3.4 Modelos de classificação

Foram utilizados três algoritmos de aprendizagem de máquina para classificar os níveis mensais de risco de dengue: Árvore de Decisão (Decision Tree), K-Vizinhos Mais Próximos (K-Nearest Neighbors — KNN) e Máquina de Vetores de Suporte (Support Vector Machine — SVM). Os modelos foram implementados em Python com a biblioteca Scikit-learn.

Para o treinamento, foram utilizadas variáveis relacionadas ao período do ano e às quantidades de casos registradas nos três meses anteriores. Essa abordagem permite que os classificadores considerem tanto a sazonalidade quanto a variação recente dos registros de dengue.

A base foi dividida cronologicamente em conjuntos de treinamento e teste, utilizando aproximadamente 70% dos registros disponíveis para treinamento e 30% para teste. Essa divisão permite avaliar os modelos em meses posteriores aos utilizados durante o treinamento, aproximando a avaliação de uma aplicação temporal.

O desempenho dos classificadores foi analisado por meio da acurácia, da precisão e da revocação (recall), além das matrizes de confusão. Essas métricas permitem comparar a quantidade de classificações corretas e observar em quais níveis de risco os modelos apresentam maior dificuldade. Os resultados dessa comparação são apresentados na seção seguinte.

## 4. Resultados e discussão

Os três modelos de classificação foram avaliados utilizando o conjunto de teste composto por 36 registros mensais. Foram consideradas as métricas de acurácia, precisão e revocação (recall), além das matrizes de confusão, para comparar o desempenho dos algoritmos na identificação dos níveis de risco de dengue.

A Árvore de Decisão e o KNN obtiveram acurácia de 55,56%, enquanto o SVM alcançou 61,11%, apresentando o melhor resultado geral entre os modelos avaliados. Considerando também a precisão e a revocação médias por classe, o SVM apresentou os maiores valores nessas duas métricas.

Apesar do desempenho superior, os resultados demonstram que os modelos ainda apresentam limitações na classificação dos níveis de risco. A distinção entre as classes baixa, média e alta nem sempre foi realizada corretamente, principalmente nos meses classificados como risco médio. Esse comportamento indica que as variáveis utilizadas não foram suficientes para distinguir adequadamente todas as categorias em parte dos registros de teste.

As matrizes de confusão permitem examinar esses erros com maior detalhe, mostrando a quantidade de meses classificados corretamente e aqueles atribuídos a categorias diferentes da classe real. Dessa forma, a comparação indica que o SVM foi o modelo com melhor desempenho nesta avaliação, mas sua acurácia de 61,11% não permite considerá-lo suficientemente confiável para uso operacional sem estudos e validações adicionais.

Os resultados devem ser interpretados considerando o caráter exploratório do projeto, a quantidade de registros mensais disponíveis e os critérios utilizados para definir as classes de risco. As categorias representam faixas de quantidade de casos estabelecidas para este estudo e não equivalem a níveis oficiais de alerta epidemiológico.

### 4.1 Análise das matrizes de confusão

As matrizes de confusão foram utilizadas para analisar o comportamento dos três classificadores em cada nível de risco. Em cada matriz, as linhas representam as classes reais e as colunas representam as classes previstas pelos modelos, seguindo a ordem: baixo, médio e alto.

A Árvore de Decisão apresentou acertos nas três classes, mas confundiu parte dos meses de risco médio com risco alto. O KNN também apresentou dificuldades para distinguir os níveis de risco baixo e médio, além de classificar incorretamente alguns meses de risco alto.

O SVM obteve sete acertos na classe de risco baixo, seis na classe de risco médio e nove na classe de risco alto. Entretanto, sete meses classificados originalmente como risco médio foram previstos como risco baixo. Além disso, alguns meses de risco alto foram classificados como baixo ou médio.

A análise demonstra que, embora o SVM tenha alcançado a maior acurácia geral, ainda existem confusões relevantes entre as categorias. Esses resultados reforçam a necessidade de interpretar as métricas em conjunto, pois uma única medida de desempenho não representa todas as dificuldades dos modelos.

## 5. Atividade de extensão

Descrever o material de divulgação produzido, os meios utilizados para compartilhá-lo, o público alcançado e as evidências coletadas.

## 6. Conclusão

O projeto teve como objetivo desenvolver e avaliar modelos de Inteligência Artificial para classificar o nível mensal de risco de dengue em Porto Velho, Rondônia, utilizando dados históricos do SINAN referentes ao período de 2016 a 2025.

Foram aplicadas etapas de coleta, preparação e análise exploratória dos dados, seguidas pelo treinamento e pela comparação de três algoritmos de classificação: Árvore de Decisão, KNN e SVM. Entre os modelos avaliados, o SVM apresentou o melhor desempenho, com acurácia de 61,11%, embora os resultados também tenham evidenciado dificuldades na distinção entre algumas classes de risco.

Conclui-se que o uso de técnicas de Inteligência Artificial permite explorar dados históricos e comparar diferentes abordagens de classificação para o estudo da dengue. Entretanto, o desempenho obtido e os critérios didáticos utilizados para definir as classes limitam a aplicação prática dos modelos. Portanto, os resultados devem ser considerados exploratórios, não constituindo um sistema validado de previsão ou alerta de surtos.

A realização do projeto permitiu aplicar conceitos de aprendizagem de máquina, análise de dados e avaliação de modelos a um problema de saúde pública, demonstrando possibilidades e limitações dessas técnicas no contexto estudado.

## 7. REFERÊNCIAS

BRASIL. Ministério da Saúde. **Dados sobre agravos de notificações**. Brasília, DF: Ministério da Saúde. Disponível em: https://www.gov.br/saude/pt-br/acesso-a-informacao/sic/dados-em-transparencia-ativa/svsa/agravos-de-notificacoes/agravos-de-notificacoes. Acesso em: 21 out. 2026.

BRASIL. Ministério da Saúde. **Sistema de Informação de Agravos de Notificação (SINAN)**. Brasília, DF: Ministério da Saúde. Disponível em: https://www.gov.br/saude/pt-br/composicao/svsa/sistemas-de-informacao/sinan/sinan. Acesso em: 21 out. 2026.

MCKINNEY, Wes et al. **pandas documentation**. Disponível em: https://pandas.pydata.org/docs/. Acesso em: 21 out. 2026.

MATPLOTLIB DEVELOPMENT TEAM. **Matplotlib documentation**. Disponível em: https://matplotlib.org/stable/. Acesso em: 21 out. 2026.

SCIKIT-LEARN DEVELOPERS. **Scikit-learn: machine learning in Python**. Disponível em: https://scikit-learn.org/stable/. Acesso em: 21 out. 2026.

## 8. Apêndices e evidências

Incluir capturas de tela, registros da divulgação e demais evidências pertinentes à atividade de extensão.