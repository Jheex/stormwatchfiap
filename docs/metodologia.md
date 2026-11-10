# Metodologia de Preparação e Análise dos Dados

## 1. Objetivo

Este documento descreve os procedimentos metodológicos utilizados no projeto StormWatch para obtenção, preparação, padronização, validação, integração e análise exploratória das bases de dados pluviométrica, hidrológica e geotécnica.

O objetivo é estabelecer um processo reproduzível, transparente e rastreável, permitindo que os dados sejam utilizados nas análises estatísticas e nas visualizações disponibilizadas pela plataforma.

## 2. Fontes e recorte dos dados

As bases utilizadas foram obtidas por meio do [Mapa Interativo do CEMADEN](https://mapainterativo.cemaden.gov.br/), considerando os seguintes filtros:

- **Unidade federativa:** São Paulo (SP).
- **Período:** janeiro de 2026.
- **Bases:** pluviométrica, hidrológica e geotécnica.

Os arquivos utilizados são:

- `dados_pluviometricos.csv`
- `dados_hidrologicos.csv`
- `dados_geotecnicos.csv`

Os arquivos originais são armazenados em `global-solution/dados/` e utilizados como entrada para o processamento realizado no notebook `global-solution/analise_stormwatch.ipynb`.

## 3. Etapas de preparação dos dados

### 3.1. Ingestão

Os três arquivos CSV são carregados no ambiente Python por meio das bibliotecas utilizadas no projeto.

A leitura é realizada preservando os arquivos originais, que servem como referência para conferência e rastreabilidade das transformações.

### 3.2. Padronização

As colunas são organizadas em uma estrutura comum, utilizando nomenclaturas padronizadas para facilitar o processamento e a integração das bases.

Entre os campos utilizados estão:

- `municipio`
- `codEstacao`
- `uf`
- `nomeEstacao`
- `latitude`
- `longitude`
- `datahora`
- `sensor`
- `valorMedida`
- `valorMedida_original`
- `status_qualidade`
- `origem`

As datas são convertidas para o formato datetime, enquanto os valores de medição são preparados para operações numéricas.

A padronização dos campos não implica confirmação automática das unidades físicas ou dos significados técnicos dos sensores.

### 3.3. Validação e qualidade

São realizadas verificações relacionadas à consistência dos registros, incluindo:

- Presença de informações necessárias para as análises.
- Conversão de datas e valores numéricos.
- Verificação de coordenadas geográficas.
- Identificação de registros duplicados.
- Identificação de valores especiais ou potencialmente inconsistentes.

As duplicidades são avaliadas e sinalizadas conforme o contexto, evitando exclusões indiscriminadas que possam comprometer a informação original.

### 3.4. Tratamento de valores especiais

Durante a preparação foram identificadas situações que exigem tratamento específico.

**Base geotécnica — valor `-1000`**

O valor `-1000`, identificado em registros de sensores de umidade, foi tratado como um valor sentinela.

Para preservar a rastreabilidade:

- O valor original é mantido em `valorMedida_original`.
- O campo analítico `valorMedida` recebe `NaN`.
- O registro é identificado por meio de `status_qualidade`.

Essa decisão evita que um valor sentinela seja interpretado como uma medição física válida.

**Base hidrológica — valor `35`**

Foi identificado o valor `35` em registros de sensores de nível hidrológico.

Como seu significado técnico ainda depende de confirmação na documentação do provedor, o valor é preservado e sinalizado para investigação.

Não é considerado automaticamente inválido nem descartado sem justificativa.

## 4. Integração das bases

### 4.1. Integração espacial

A integração espacial considera as coordenadas geográficas das estações.

É utilizado o cálculo de distância geográfica pelo método de Haversine para identificar estações coincidentes ou próximas.

As correspondências são classificadas conforme sua condição:

- **Exata:** quando as coordenadas correspondem.
- **Aproximada:** quando existe proximidade geográfica, mas não há coincidência exata.

As associações aproximadas são identificadas separadamente, pois a proximidade entre estações não garante que representem as mesmas condições ambientais.

### 4.2. Integração temporal

A integração temporal considera a identificação da estação e a data/hora da observação.

São utilizados registros com correspondência de estação e timestamp idênticos.

Não são aplicadas automaticamente:

- Interpolação temporal.
- Preenchimento de observações ausentes.
- Aproximação de horários.
- Estimativas de medições não registradas.

Essa abordagem evita criar correspondências artificiais entre observações realizadas em momentos diferentes.

## 5. Análises exploratórias

Após a preparação, os dados são utilizados em análises estatísticas e visualizações.

Entre os procedimentos realizados estão:

- Estatística descritiva, incluindo medidas de tendência central e dispersão.
- Análise de distribuição e comparação entre municípios e sensores.
- Visualizações da evolução temporal das medições.
- Identificação de relações entre variáveis.
- Cálculo de correlação de Pearson e Spearman.
- Análise de probabilidade condicional, utilizando percentis como referências estatísticas.

Os resultados são interpretados considerando as características, limitações e qualidade das bases utilizadas.

As correlações identificadas representam associações estatísticas e não comprovam, isoladamente, relações de causalidade.

Da mesma forma, percentis e probabilidades calculadas no projeto são referências exploratórias, não equivalendo a limites oficiais de alerta.

## 6. Geração dos dados para o dashboard

Após a execução das etapas de processamento e análise no notebook, os resultados consolidados são exportados para:

`data/dashboard/resumo.json`

Esse arquivo contém os metadados do período analisado, informações agregadas e registros utilizados pela interface.

O dashboard consome o JSON por meio dos arquivos JavaScript do projeto, permitindo apresentar os resultados sem executar o notebook diretamente durante a navegação.

## 7. Reprodutibilidade

Para reproduzir o processamento:

1. Obter as três bases no Mapa Interativo do CEMADEN, utilizando os filtros correspondentes ao estudo.
2. Salvar os arquivos CSV em `global-solution/dados/`, mantendo os nomes esperados pelo notebook.
3. Instalar as dependências Python descritas em `requirements.txt`.
4. Abrir `global-solution/analise_stormwatch.ipynb`.
5. Executar as células na sequência apresentada, preferencialmente após reiniciar o kernel.
6. Verificar a geração do arquivo `data/dashboard/resumo.json`.
7. Disponibilizar os arquivos do projeto por meio do servidor de desenvolvimento ou da hospedagem configurada.

A reprodução dos resultados depende da utilização dos arquivos de entrada correspondentes ao mesmo recorte temporal e geográfico.

## 8. Interpretação responsável

O StormWatch possui finalidade exploratória e informativa.

Por isso, são adotados os seguintes princípios:

- Não atribuir unidades físicas sem documentação técnica.
- Não interpretar valores sentinela como medições válidas.
- Não eliminar valores suspeitos sem justificativa.
- Não considerar correlação estatística como comprovação de causalidade.
- Identificar correspondências espaciais aproximadas.
- Não criar limites oficiais de risco sem referências documentadas.
- Informar que os dados analisados são históricos e correspondem a janeiro de 2026.

Os resultados da plataforma não substituem os comunicados, alertas ou avaliações oficiais dos órgãos responsáveis.