# Dicionário de Dados e Metadados

Este documento apresenta a descrição dos campos utilizados na padronização das bases pluviométrica, hidrológica e geotécnica do projeto StormWatch.

O dicionário reúne os nomes padronizados das variáveis, suas respectivas descrições, unidades de medida e observações relacionadas ao tratamento e à interpretação dos dados.

As três bases utilizadas foram obtidas por meio do [Mapa Interativo do CEMADEN](https://mapainterativo.cemaden.gov.br/), considerando os dados referentes ao estado de São Paulo, no período de janeiro de 2026.

**Importante:** a padronização dos nomes e formatos das colunas não representa uma validação integral dos seus significados físicos. As unidades de medida, convenções temporais, escalas e referências dos sensores devem ser confirmadas com a documentação técnica oficial do CEMADEN. Quando essas informações não estão disponíveis ou não foram confirmadas, são identificadas como pendentes.

## 1. Dicionário de campos padronizados

| Campo padronizado | Descrição | Unidade | Observações |
|---|---|---|---|
| `municipio` | Município ao qual a estação de monitoramento está associada. | Não aplicável | Informação preservada conforme o arquivo de origem. |
| `codEstacao` | Código identificador da estação de monitoramento. | Não aplicável | Utilizado como referência para identificação e relacionamento entre registros. |
| `uf` | Unidade federativa onde a estação está localizada. | Sigla | Para este estudo, o recorte geográfico corresponde ao estado de São Paulo (SP). |
| `nomeEstacao` | Nome ou identificação nominal da estação de monitoramento. | Não aplicável | Mantido conforme a identificação disponibilizada na base original. |
| `latitude` | Coordenada geográfica que representa a posição da estação no sentido norte-sul. | Graus decimais | Datum geodésico e precisão das coordenadas dependem de confirmação na documentação do provedor. |
| `longitude` | Coordenada geográfica que representa a posição da estação no sentido leste-oeste. | Graus decimais | Datum geodésico e precisão das coordenadas dependem de confirmação na documentação do provedor. |
| `datahora` | Data e horário associados à observação registrada pelo sistema de monitoramento. | Data/hora | O fuso horário e a convenção de registro não foram confirmados. |
| `sensor` | Identificação ou classificação do sensor responsável pela medição, quando disponível. | Não aplicável | A interpretação dos códigos e tipos de sensores depende da documentação técnica correspondente. |
| `valorMedida` | Valor numérico utilizado nas análises após a padronização e aplicação das regras de tratamento. | A confirmar | A unidade e o significado físico variam conforme a base e o tipo de sensor. |
| `valorMedida_original` | Representação original do valor de medição antes das conversões ou ajustes aplicados no tratamento. | Conforme origem | Mantido para garantir rastreabilidade e possibilitar a comparação com o dado recebido. |
| `status_qualidade` | Indicador utilizado para registrar o resultado das verificações de qualidade aplicadas aos dados. | Não aplicável | Pode identificar registros válidos, valores sentinela, possíveis inconsistências ou situações que exigem investigação. |
| `origem` | Identificação da base de dados da qual o registro foi obtido. | Não aplicável | Classificada como pluviométrica, hidrológica ou geotécnica. |

## 2. Particularidades das bases de dados

Embora os campos tenham sido padronizados para facilitar o processamento e a integração, cada conjunto de dados possui características próprias.

### 2.1. Base pluviométrica

Contém registros relacionados ao monitoramento de precipitação nas estações disponibilizadas pelo CEMADEN.

A interpretação dos valores depende da confirmação da unidade de medida e do intervalo de acumulação utilizado pelo sistema de monitoramento.

### 2.2. Base hidrológica

Reúne medições associadas ao monitoramento hidrológico, incluindo registros de sensores de nível.

Durante o tratamento, foi identificado o valor `35` em registros de nível hidrológico. Esse valor foi preservado e sinalizado para investigação, sem que fosse atribuído a ele um significado físico ou uma classificação de anomalia definitiva.

### 2.3. Base geotécnica

Contém medições associadas ao monitoramento geotécnico, incluindo sensores de umidade instalados em diferentes profundidades.

Foi identificado o valor `-1000` em registros dessa base. Para preservar a rastreabilidade, o valor original foi mantido em `valorMedida_original`, enquanto `valorMedida` recebeu `NaN` para representar a ausência de um valor numérico válido para as análises. O registro também foi identificado por meio de `status_qualidade`.

## 3. Regras de interpretação e qualidade

Para evitar interpretações indevidas durante as análises, foram adotados os seguintes princípios:

- **Preservação da origem:** os valores originais são mantidos sempre que necessário para permitir a rastreabilidade das transformações.
- **Padronização:** os campos foram organizados em uma nomenclatura comum para facilitar o processamento das três bases.
- **Tratamento de valores especiais:** valores potencialmente inválidos ou que exigem investigação são identificados sem atribuição automática de significado.
- **Ausência de inferência de unidades:** nenhuma unidade física é atribuída exclusivamente com base no nome de uma coluna ou na magnitude de um valor.
- **Rastreabilidade:** as regras aplicadas durante o tratamento são registradas por meio dos campos auxiliares, especialmente `valorMedida_original` e `status_qualidade`.

## 4. Pendências de documentação técnica

Para ampliar a precisão e a confiabilidade das análises, permanecem necessárias as seguintes confirmações junto à documentação oficial do provedor:

| Base | Informação pendente | Relevância para o projeto |
|---|---|---|
| Pluviométrica | Unidade de medida da precipitação e intervalo de acumulação. | Permite interpretar corretamente os volumes registrados e comparar medições. |
| Hidrológica | Unidade de medida, referência e convenção dos níveis monitorados. | Necessário para interpretar os valores de nível e avaliar sua relação com eventos de chuva. |
| Hidrológica | Significado técnico do valor `35` identificado nos registros. | Permite determinar se representa uma medição válida, um código especial ou outra condição. |
| Geotécnica | Unidade de medida, escala e significado dos sensores de umidade por profundidade. | Necessário para interpretar as condições do solo e comparar sensores. |
| Todas | Fuso horário, convenção de registro temporal e frequência esperada das medições. | Importante para a integração temporal e análise da evolução dos eventos. |
| Todas | Critérios oficiais de qualidade, limites de alerta e respectivas fontes responsáveis. | Necessário para diferenciar análises estatísticas exploratórias de classificações oficiais de risco. |

## 5. Considerações finais

O presente dicionário estabelece uma referência comum para a interpretação dos campos utilizados no StormWatch, documentando a estrutura dos dados e os procedimentos de padronização adotados.

As informações ainda não confirmadas são explicitamente identificadas como pendências, evitando atribuições de unidades, significados ou limites que não estejam respaldados por documentação técnica.

Dessa forma, o projeto mantém a rastreabilidade das informações e estabelece uma base documental para futuras atualizações, validações e aprimoramentos das análises ambientais.