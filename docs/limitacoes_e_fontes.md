# Fontes de Dados, Limitações e Decisões Metodológicas

## 1. Fontes de dados

O projeto StormWatch utiliza três conjuntos de dados ambientais obtidos por meio do [Mapa Interativo do CEMADEN](https://mapainterativo.cemaden.gov.br/).

As bases foram selecionadas considerando o estado de São Paulo e o período de janeiro de 2026.

| Arquivo | Categoria | Finalidade |
|---|---|---|
| `dados_pluviometricos.csv` | Pluviométrica | Análise de registros relacionados à precipitação. |
| `dados_hidrologicos.csv` | Hidrológica | Análise de medições relacionadas ao monitoramento hidrológico. |
| `dados_geotecnicos.csv` | Geotécnica | Análise de medições relacionadas às condições do solo. |

Os arquivos são armazenados no diretório `global-solution/dados/` e utilizados como entrada para o notebook de processamento.

**Fonte institucional:** Centro Nacional de Monitoramento e Alertas de Desastres Naturais (CEMADEN).

**Portal de acesso:** https://mapainterativo.cemaden.gov.br/

**Recorte geográfico:** Estado de São Paulo (SP).

**Recorte temporal:** janeiro de 2026.

A data específica de obtenção dos arquivos, a licença de utilização e os metadados técnicos detalhados devem ser registrados após confirmação nas informações oficiais disponibilizadas pelo provedor.

## 2. Limitações dos dados

A utilização das bases exige atenção a algumas limitações que podem influenciar a interpretação dos resultados.

### 2.1. Limitação temporal

O estudo utiliza registros referentes a janeiro de 2026.

Portanto, os resultados representam um recorte histórico específico e não constituem monitoramento em tempo real.

Não é possível extrapolar automaticamente os resultados para outros períodos ou utilizá-los como previsão de eventos futuros.

### 2.2. Unidades de medida não confirmadas

As unidades físicas de todas as variáveis não foram confirmadas integralmente na documentação técnica consultada.

Essa limitação exige cautela na interpretação dos valores e impede atribuir unidades específicas sem respaldo documental.

As pendências incluem:

- Unidade de precipitação e intervalo de acumulação.
- Unidade e referência dos níveis hidrológicos.
- Unidade e escala dos sensores geotécnicos de umidade.
- Convenções técnicas associadas aos diferentes tipos de sensores.

### 2.3. Convenção temporal

Os arquivos não apresentam confirmação suficiente sobre o fuso horário e a convenção utilizada para registrar os horários das medições.

Essa condição pode influenciar comparações temporais e a integração entre bases.

Por esse motivo, o projeto utiliza correspondências temporais estritas, sem aplicar aproximações ou conversões de fuso não documentadas.

### 2.4. Valores especiais e qualidade

Foram identificadas situações que exigem atenção durante a interpretação:

**Valor `-1000` na base geotécnica**

Identificado em registros de sensores de umidade e tratado como valor sentinela no campo analítico.

O valor original é preservado para rastreabilidade, enquanto a medição correspondente é representada como ausente (`NaN`) nas análises.

**Valor `35` na base hidrológica**

Identificado em registros de nível hidrológico.

Seu significado técnico ainda requer confirmação com a documentação do sensor ou do provedor. Por isso, o valor é preservado e sinalizado para investigação, sem classificação definitiva de validade ou invalidade.

### 2.5. Correspondências espaciais

A integração espacial considera a localização geográfica das estações.

Durante o processamento, foram identificadas duas correspondências geotécnicas com pluviômetros classificadas como aproximadas.

Essas associações não devem ser interpretadas como equivalência de localização ou garantia de representatividade ambiental.

A proximidade geográfica não assegura que duas estações registrem as mesmas condições locais.

### 2.6. Limitações das análises estatísticas

As análises de correlação, distribuição e probabilidade condicional são exploratórias.

Os resultados dependem da disponibilidade, qualidade, representatividade e características dos registros utilizados.

Correlação não comprova causalidade, e probabilidades calculadas a partir do recorte estudado não devem ser generalizadas automaticamente para outras regiões ou períodos.

Também não foram estabelecidos limites oficiais de alerta a partir dos dados disponíveis.

## 3. Decisões metodológicas para transparência

Para reduzir interpretações indevidas e preservar a confiabilidade do processamento, foram adotadas as seguintes decisões:

| Situação | Decisão adotada |
|---|---|
| Arquivos originais | Preservar os CSVs recebidos como referência para rastreabilidade. |
| Padronização | Utilizar nomenclatura comum para facilitar o processamento das bases. |
| Valores sentinela | Identificar e tratar conforme sua natureza, preservando o valor original. |
| Valores suspeitos | Sinalizar para investigação, evitando exclusões sem justificativa. |
| Duplicidades | Verificar e documentar sem eliminar indiscriminadamente. |
| Integração espacial | Diferenciar correspondências exatas e aproximadas. |
| Integração temporal | Exigir correspondência de estação e timestamp idênticos. |
| Unidades não confirmadas | Evitar atribuições sem documentação técnica. |
| Limites de alerta | Não criar classificações oficiais sem referências dos órgãos responsáveis. |

## 4. Uso responsável da plataforma

O StormWatch foi desenvolvido como uma iniciativa CitizenTech, com a finalidade de organizar, analisar e apresentar informações ambientais de maneira acessível.

A plataforma busca contribuir para a compreensão dos dados e incentivar o uso de informações públicas em análises exploratórias.

Entretanto:

- Os resultados não representam alertas oficiais.
- A plataforma não substitui o monitoramento institucional.
- As análises não devem ser utilizadas isoladamente para decisões de segurança ou evacuação.
- A ausência de registros não significa ausência de risco.
- As informações devem ser interpretadas considerando o período e as limitações das bases utilizadas.

Em situações de risco, devem prevalecer as orientações e os comunicados dos órgãos oficiais de monitoramento e defesa civil.

## 5. Pendências para atualização documental

As seguintes informações devem ser confirmadas para aprimorar a documentação do projeto:

- Data de acesso e obtenção de cada arquivo.
- Condições de uso e licença aplicável aos dados.
- Unidades oficiais das medições pluviométricas.
- Unidade e referência dos níveis hidrológicos.
- Significado técnico do valor `35`.
- Escala e unidades dos sensores geotécnicos.
- Fuso horário e frequência de aquisição dos registros.
- Critérios oficiais de qualidade e limites de alerta.

As pendências devem ser atualizadas somente após confirmação em documentação institucional ou técnica confiável.

## 6. Referência institucional

**Centro Nacional de Monitoramento e Alertas de Desastres Naturais (CEMADEN)**

Mapa Interativo do CEMADEN:

https://mapainterativo.cemaden.gov.br/

Os dados utilizados no StormWatch foram obtidos por meio desse portal, respeitando o recorte geográfico e temporal definido para o estudo.