# 🌧️ StormWatch
### Tecnologia, dados e cidadania na prevenção de riscos ambientais

<p align="center">
  <strong>Uma solução CitizenTech que transforma dados ambientais em informação acessível.</strong>
</p>

<p align="center">
  <a href="https://stormwatchfiap-68rb.vercel.app/">Acessar plataforma</a>
  <a href="https://N/A">Video Pitch</a>
  <a href="https://github.com/Jheex/stormwatchfiap">Repositório GitHub</a>
  <a href="https://colab.research.google.com/github/Jheex/stormwatchfiap/blob/main/global-solution/analise_stormwatch.ipynb">Google Colab</a>
</p>

## 👥 Equipe e créditos

Desenvolvido colaborativamente por:

- Jhonatan Lima Coelho
- João Torres de Brito
- Kewyn Montani Zancope
- Mariana Miyasaka Maruyama
- Thiago Rodrigues Pereira Santos

**Instituição:** FIAP  
**Projeto:** Global Solution — 2º Semestre de 2026

---

## 🌎 Sobre o projeto

O **StormWatch** é uma plataforma de análise e visualização de dados ambientais desenvolvida como parte da **Global Solution do segundo semestre de 2026 da FIAP**.

O projeto utiliza conceitos de Data Science, análise estatística e desenvolvimento web para organizar e apresentar informações relacionadas ao monitoramento pluviométrico, hidrológico e geotécnico.

A proposta é transformar conjuntos de dados ambientais em informações mais acessíveis, permitindo que a população compreenda melhor as condições monitoradas e tenha contato com informações que contribuam para a conscientização e a prevenção de riscos ambientais.

Por meio de um dashboard interativo e de análises desenvolvidas em Python, o StormWatch busca aproximar a tecnologia das necessidades da sociedade.

> **Nossa missão:** colocar o cidadão no centro da tecnologia, transformando dados ambientais em conhecimento para contribuir com cidades mais conscientes, preparadas e sustentáveis.

## 🎯 Problema e oportunidade

Enchentes, alagamentos e deslizamentos representam desafios importantes para a segurança da população, especialmente em regiões sujeitas a eventos climáticos intensos e alterações nas condições ambientais.

Informações sobre precipitação, nível da água e condições do solo podem ajudar a compreender diferentes aspectos desses fenômenos.

Entretanto, dados provenientes de diferentes fontes podem apresentar formatos, estruturas e características distintas, dificultando sua interpretação conjunta.

O StormWatch propõe uma solução tecnológica para:

- Organizar dados ambientais provenientes de diferentes bases.
- Padronizar informações para facilitar sua análise.
- Investigar relações entre variáveis ambientais.
- Apresentar indicadores e visualizações de maneira acessível.
- Aproximar informações técnicas da população.
- Incentivar a conscientização sobre prevenção de riscos ambientais.

## 💡 A solução StormWatch

A plataforma trabalha com três conjuntos de dados ambientais:

| Base de dados | Informações analisadas |
|---|---|
| 🌧️ Pluviométrica | Registros relacionados à precipitação e ao comportamento das chuvas. |
| 🌊 Hidrológica | Informações de sensores relacionados à chuva e ao nível da água. |
| 🌱 Geotécnica | Informações de sensores relacionados às condições do solo, incluindo umidade em diferentes profundidades. |

Os dados são submetidos a procedimentos de preparação, validação, tratamento e análise estatística.

Os resultados são organizados em um arquivo JSON, utilizado pelo dashboard para apresentar indicadores, gráficos, filtros e tabelas.

### Principais funcionalidades

- Dashboard interativo com indicadores gerais.
- Alternância entre as três fontes de dados e visão integrada.
- Filtros por município, estação e sensor.
- Visualização da evolução diária dos registros.
- Comparação de métricas estatísticas.
- Gráfico de distribuição por sensores.
- Tabela de informações agrupadas por município.
- Página de metodologia e documentação.
- Apresentação dos impactos sociais e da proposta CitizenTech.

## 📊 Dashboard

O dashboard é a principal interface de exploração das informações do StormWatch.

Ele permite consultar os registros disponíveis, selecionar diferentes fontes e aplicar filtros para observar os dados de acordo com o município, a estação e o sensor.

### Indicadores apresentados

- Total de registros.
- Quantidade de estações.
- Municípios abrangidos.
- Dias contemplados pela base.

### Visualizações

- Evolução temporal dos registros.
- Distribuição dos dados por sensor.
- Comparação de informações por município.
- Indicadores atualizados conforme os filtros selecionados.

**Acesse a plataforma:** https://stormwatchfiap-68rb.vercel.app/

## 🧪 Dados e fontes de informação

As três bases utilizadas no projeto foram obtidas por meio do **Mapa Interativo do CEMADEN**.

**Fonte:** https://mapainterativo.cemaden.gov.br/

Os arquivos utilizados são:

- `dados_pluviometricos.csv`
- `dados_hidrologicos.csv`
- `dados_geotecnicos.csv`

### Recorte temporal

| Característica | Informação |
|---|---|
| Região analisada | Estado de São Paulo (SP) |
| Período | 01/01/2026 a 31/01/2026 |
| Frequência | Conforme os registros disponibilizados pelos sensores |
| Formato original | CSV |
| Fonte | Mapa Interativo do CEMADEN |

Os arquivos foram selecionados considerando o recorte de janeiro de 2026 e os filtros utilizados na plataforma de origem.

### Preparação e qualidade dos dados

O processamento contempla:

1. Carregamento das bases originais.
2. Inspeção da estrutura e dos tipos de dados.
3. Verificação de valores ausentes e registros duplicados.
4. Padronização de datas e valores numéricos.
5. Identificação dos tipos de sensores.
6. Investigação de valores suspeitos ou sentinelas.
7. Preparação dos dados para análises estatísticas.
8. Integração de informações compatíveis.
9. Exportação dos resultados para JSON.

### Tratamentos específicos

Algumas situações identificadas durante a análise exigem cuidados especiais:

- **Valor `-1000` na base geotécnica:** tratado como valor sentinela nos registros de umidade do solo. O valor original é preservado para rastreabilidade, enquanto a coluna analítica recebe um valor ausente (`NaN`).
- **Valor `35` na base hidrológica:** preservado e sinalizado para investigação. Como não existe confirmação suficiente de que seja inválido, ele não é descartado automaticamente.
- **Registros duplicados:** são verificados e documentados, sem exclusão automática indiscriminada.
- **Dados ausentes:** são identificados e tratados conforme a finalidade de cada análise.

As decisões de tratamento buscam preservar a integridade das informações e evitar conclusões baseadas em valores cuja interpretação não esteja confirmada.

## 📈 Análises estatísticas e técnicas aplicadas

O notebook `analise_stormwatch.ipynb` concentra o processamento e as análises realizadas com Python.

### 1. Estatística descritiva

São utilizadas medidas estatísticas para compreender o comportamento dos dados:

- Média.
- Mediana.
- Quartis.
- Valores mínimos e máximos.
- Contagem de registros.
- Distribuição das medições por grupos.

As comparações são realizadas considerando municípios, estações, sensores e períodos.

### 2. Visualização de dados

São utilizados gráficos para facilitar a interpretação das informações:

- Gráficos de barras.
- Gráficos de linhas.
- Boxplots.
- Distribuições por categoria de sensor.
- Evolução temporal das medições.

### 3. Integração de bases de dados

As informações pluviométricas e hidrológicas são relacionadas para investigar registros que compartilham identificadores de estação e horários compatíveis.

A integração considera a correspondência entre estações e timestamps, permitindo analisar relações entre diferentes medições ambientais.

Correspondências aproximadas são identificadas separadamente e não são consideradas equivalentes a correspondências exatas.

### 4. Correlação de Pearson e Spearman

São utilizadas duas medidas de correlação:

- **Pearson:** investiga a intensidade e a direção da relação linear entre duas variáveis.
- **Spearman:** investiga a relação monotônica considerando a ordenação dos valores.

As análises investigam associações entre medições pluviométricas e hidrológicas.

Os resultados são interpretados com cautela, considerando a quantidade de observações e a possibilidade de dependência entre as fontes.

### 5. Probabilidade condicional

A análise investiga probabilidades relacionadas à ocorrência de chuva e a níveis hidrológicos elevados.

O percentil 75 é utilizado como referência estatística para identificar os maiores valores de nível observados no conjunto analisado.

Também é realizada uma comparação entre cenários com todos os registros e cenários sem os registros de nível iguais a `35`, a fim de investigar a influência desses valores nos resultados.

Essa abordagem é exploratória e não representa um limiar oficial de alerta.

## 🔄 Fluxo de processamento e integração

O StormWatch utiliza o notebook Python como ambiente central de preparação e análise dos dados.

O fluxo de funcionamento é:

```text
       MAPA INTERATIVO DO CEMADEN
                   |
                   v
          Arquivos CSV originais
                   |
                   v
           Notebook Jupyter
                   |
          +--------+--------+
          |                 |
          v                 v
      Preparação        Validação
          |                 |
          +--------+--------+
                   |
                   v
          Análise estatística
                   |
                   v
        Exportação para JSON
                   |
                   v
       data/dashboard/resumo.json
                   |
                   v
           Dashboard Web
                   |
                   v
       Visualização interativa
```

### Geração do JSON

Após a preparação das bases, o notebook executa a seção **3.9 — Exportando dados em JSON**.

Essa etapa reúne os registros das três fontes, realiza a agregação das informações e gera o arquivo:

`data/dashboard/resumo.json`

O JSON contém:

- Período analisado.
- Metadados das fontes.
- Quantidade total de registros.
- Quantidade de registros agregados.
- Informações agrupadas por fonte, data, município, estação e sensor.

O dashboard consome diretamente esse arquivo por meio de JavaScript, sem precisar executar novamente o processamento Python durante a navegação.

**Importante:** quando os dados forem atualizados, será necessário executar novamente o notebook e disponibilizar a nova versão do JSON para que o dashboard apresente os resultados atualizados.

## 🛠️ Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Preparação e análise dos dados. |
| Jupyter Notebook | Ambiente de desenvolvimento das análises. |
| Pandas | Manipulação e organização dos dados. |
| NumPy | Operações numéricas e tratamento de valores. |
| SciPy | Recursos para análises estatísticas. |
| Matplotlib | Construção de visualizações. |
| Seaborn | Visualizações estatísticas. |
| HTML5 | Estrutura das páginas web. |
| CSS3 | Estilização e responsividade. |
| JavaScript | Interatividade e processamento dos dados no navegador. |
| Chart.js | Construção dos gráficos do dashboard. |
| JSON | Comunicação entre o processamento Python e a interface web. |
| CSV | Armazenamento dos dados originais. |
| Git e GitHub | Versionamento e hospedagem do código-fonte. |
| Vercel | Publicação da aplicação web. |

## 📁 Estrutura do repositório

```text
stormwatchfiap/
│
├── index.html
├── README.md
├── requirements.txt
│
├── assets/
│   ├── css/
│   │   ├── dashboard.css
│   │   └── style.css
│   │
│   ├── img/
│   │   └── logotipo.webp
│   │
│   └── js/
│       ├── dashboard.js
│       └── main.js
│
├── data/
│   └── dashboard/
│       └── resumo.json
│
├── docs/
│   ├── dicionario_dados.md
│   ├── limitacoes_e_fontes.md
│   └── metodologia.md
│
├── global-solution/
│   ├── analise_stormwatch.ipynb
│   │
│   └── dados/
│       ├── dados_geotecnicos.csv
│       ├── dados_hidrologicos.csv
│       └── dados_pluviometricos.csv
│
├── includes/
│   ├── header.html
│   └── footer.html
│
└── pages/
    ├── dashboard.html
    ├── impacto.html
    ├── metodologia.html
    └── notebook.html
```

## ⚙️ Como executar o projeto localmente

### 1. Pré-requisitos

Para executar o projeto, recomenda-se ter:

- Python 3.10 ou superior.
- Visual Studio Code.
- Extensão Jupyter para o VS Code.
- Extensão Live Server para o VS Code.
- Git.

### 2. Clonar o repositório

```bash
git clone https://github.com/Jheex/stormwatchfiap.git
```

Acesse a pasta:

```bash
cd stormwatchfiap
```

### 3. Criar um ambiente virtual

```bash
python -m venv .venv
```

No Windows, ative o ambiente:

```powershell
.venv\Scripts\Activate.ps1
```

No Linux ou macOS:

```bash
source .venv/bin/activate
```

### 4. Instalar as dependências

```bash
pip install -r requirements.txt
```

As bibliotecas utilizadas no notebook incluem Pandas, NumPy, Matplotlib, Seaborn, SciPy e Jupyter.

### 5. Preparar os arquivos de dados

Os três arquivos CSV devem estar disponíveis na pasta:

```text
global-solution/dados/
```

Com os seguintes nomes:

```text
dados_pluviometricos.csv
dados_hidrologicos.csv
dados_geotecnicos.csv
```

Os arquivos devem ser obtidos na fonte de dados indicada pelo projeto, respeitando o mesmo recorte e os filtros utilizados nas análises.

### 6. Executar o notebook

Abra o arquivo:

```text
global-solution/analise_stormwatch.ipynb
```

Utilize o ambiente virtual criado anteriormente como kernel do Jupyter.

Execute as células em ordem, desde o carregamento das bases até a seção:

**3.9 — Exportando dados em JSON**

A execução completa permite reproduzir as etapas de preparação, análise e geração do arquivo consumido pelo dashboard.

Ao final, verifique se o arquivo foi criado em:

```text
data/dashboard/resumo.json
```

### 7. Executar a aplicação web

Abra a pasta do projeto no Visual Studio Code.

Localize o arquivo `index.html`, clique com o botão direito e selecione:

**Open with Live Server**

O navegador abrirá a plataforma StormWatch.

Recomenda-se utilizar um servidor local porque a aplicação carrega componentes HTML e arquivos JSON por meio de requisições `fetch()`. Abrir os arquivos diretamente pelo navegador pode impedir o funcionamento desses recursos.

## 📚 Documentação complementar

O repositório possui documentos destinados a explicar os procedimentos e as decisões tomadas durante o desenvolvimento.

| Documento | Descrição |
|---|---|
| `docs/metodologia.md` | Descreve as etapas de preparação, validação, tratamento e integração dos dados. |
| `docs/dicionario_dados.md` | Apresenta os campos utilizados e os metadados disponíveis, incluindo pendências de confirmação. |
| `docs/limitacoes_e_fontes.md` | Registra as fontes, limitações conhecidas e decisões de tratamento. |

## ⚠️ Limitações e uso responsável

O StormWatch é um projeto acadêmico de análise e visualização de dados ambientais.

Os resultados devem ser interpretados considerando as seguintes limitações:

- O conjunto analisado corresponde ao período de janeiro de 2026.
- Os dados utilizados são históricos e não representam monitoramento em tempo real.
- Nem todas as unidades de medida foram confirmadas pela documentação disponível.
- O fuso horário das observações não está explicitamente informado nos arquivos de origem.
- O significado do valor hidrológico `35` ainda exige investigação.
- A proximidade geográfica entre estações não garante equivalência das condições ambientais.
- Correlações estatísticas não demonstram, isoladamente, relações de causa e efeito.
- A ausência de limiares oficiais impede a classificação validada de níveis de risco.

### Privacidade e responsabilidade

O projeto trabalha com informações relacionadas a estações e medições ambientais.

A apresentação dos dados deve respeitar a finalidade pública e acadêmica da análise, evitando a exposição desnecessária de informações pessoais ou a associação indevida de registros ambientais a indivíduos.

### Aviso importante

**O StormWatch não substitui sistemas oficiais de monitoramento, previsão meteorológica ou emissão de alertas da Defesa Civil.**

A plataforma não deve ser utilizada isoladamente para decisões relacionadas à segurança da população.

Em situações de risco, devem ser acompanhadas as orientações e os comunicados dos órgãos oficiais competentes.

## 🌱 Impacto social e CitizenTech

O conceito de CitizenTech propõe utilizar a tecnologia para atender às necessidades da sociedade e ampliar o acesso à informação.

O StormWatch aplica esse conceito ao organizar dados ambientais e apresentá-los por meio de uma interface acessível.

A iniciativa busca contribuir para:

- Democratização do acesso à informação ambiental.
- Conscientização sobre fenômenos climáticos.
- Incentivo à cultura de prevenção.
- Aproximação entre tecnologia, cidadania e sustentabilidade.
- Desenvolvimento de soluções digitais voltadas ao interesse coletivo.

Acreditamos que informações compreensíveis e acessíveis podem contribuir para uma sociedade mais consciente e participativa.

## 🚀 Possibilidades de evolução

O projeto poderá ser ampliado futuramente por meio de:

- Incorporação de novos períodos de dados.
- Integração com outras fontes ambientais oficiais.
- Atualização automatizada das bases.
- Aprimoramento das análises estatísticas.
- Desenvolvimento de indicadores ambientais.
- Estudos de tendências temporais.
- Melhorias de acessibilidade e experiência do usuário.
- Investigação de modelos preditivos, mediante dados adequados e validação técnica.
- Integração futura com informações oficiais de monitoramento e alertas.

Essas possibilidades dependem da disponibilidade de dados, documentação técnica e critérios de validação apropriados.

---

<p align="center">
  <strong>🌧️ StormWatch</strong>
  <br />
  Tecnologia a serviço da sociedade.
  <br /><br />
  Prevenção · Informação · Cidadania
</p>