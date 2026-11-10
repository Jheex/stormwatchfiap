# 🌧️ StormWatch
### Tecnologia, dados e cidadania na prevenção de riscos ambientais

<p align="center">
  **Uma solução CitizenTech para transformar dados ambientais em informação acessível à população.**
</p>

---

## 🌎 Sobre o projeto

O **StormWatch** é uma plataforma de monitoramento e análise de dados ambientais desenvolvida como parte da Global Solution do segundo semestre de 2026 da FIAP.

O projeto tem como objetivo utilizar Data Science, inovação e tecnologia para contribuir com a compreensão de fenômenos ambientais associados a enchentes e deslizamentos.

A plataforma organiza, trata e integra dados pluviométricos, hidrológicos e geotécnicos, apresentando informações por meio de um Dashboard interativo.

Mais do que visualizar números, buscamos aproximar os dados da sociedade, facilitando o acesso à informação e incentivando uma cultura de prevenção.

> **Nossa missão:** colocar o cidadão no centro da tecnologia, transformando dados ambientais em conhecimento que contribua para cidades mais seguras, conscientes e sustentáveis.

## 🎯 Problema que queremos ajudar a enfrentar

Enchentes e deslizamentos representam desafios importantes para a segurança das comunidades, especialmente em regiões vulneráveis a eventos climáticos e alterações nas condições ambientais.

O acesso a informações organizadas sobre chuva, nível dos rios e condições geotécnicas pode contribuir para uma melhor compreensão desses fenômenos.

O StormWatch propõe uma abordagem baseada em dados para:

- Organizar informações ambientais provenientes de diferentes fontes.
- Facilitar a interpretação de dados por meio de visualizações.
- Aproximar informações técnicas da população.
- Incentivar a conscientização sobre prevenção de riscos ambientais.
- Demonstrar como a tecnologia pode contribuir para o bem-estar coletivo.

## 💡 Nossa solução

O StormWatch reúne três conjuntos de informações ambientais:

| Área | Informações analisadas |
|---|---|
| 🌧️ Pluviometria | Dados relacionados à precipitação. |
| 🌊 Hidrologia | Dados relacionados ao monitoramento hidrológico. |
| 🌱 Geotecnia | Dados relacionados ao monitoramento geotécnico. |

Essas informações passam por etapas de tratamento, padronização e integração, sendo posteriormente disponibilizadas para consulta no Dashboard.

## 📊 Dashboard

O Dashboard é a principal interface de exploração dos dados do StormWatch.

Entre suas funcionalidades estão:

- Visualização de indicadores gerais.
- Filtro por município.
- Filtro por estação.
- Filtro por sensor.
- Gráfico de evolução temporal.
- Gráfico de distribuição dos registros por sensor.
- Tabela de informações por município.

A proposta é permitir que o usuário explore os dados de maneira simples e compreenda melhor as informações ambientais disponíveis.

## 🧪 Dados e processamento

O projeto utiliza arquivos CSV como fontes de dados e um pipeline desenvolvido em Python para realizar o tratamento e a integração das informações.

### Volume de dados

Os arquivos de origem utilizados atualmente apresentam os seguintes volumes:

| Conjunto de dados | Registros | Estações | Municípios |
|---|---:|---:|---:|
| Pluviométricos | 468.164 | 546 | 193 |
| Geotécnicos | 244.449 | 18 | 8 |
| Hidrológicos | 25.072 | 22 | 20 |
| **Total** | **737.685** | — | — |

**Período dos dados:** 01/01/2026 a 31/01/2026.

O catálogo integrado reúne 548 estações únicas.

### Etapas do pipeline

O processamento realizado pelo script `scripts/preparar_dados.py` contempla:

1. Leitura dos arquivos CSV originais.
2. Tratamento e padronização dos dados.
3. Identificação de valores ausentes e códigos especiais.
4. Verificação da qualidade e consistência dos registros.
5. Correspondência espacial entre estações.
6. Integração dos conjuntos de dados.
7. Geração de arquivos tratados e integrados.
8. Criação do resumo JSON utilizado pelo Dashboard.

### Integração espacial e temporal

A correspondência entre estações considera suas coordenadas geográficas, utilizando o cálculo de distância pelo método de Haversine.

As correspondências são classificadas como exatas ou aproximadas. Correspondências aproximadas são mantidas identificadas como tal, sem pressupor que estações próximas representem necessariamente as mesmas condições ambientais.

A integração temporal utiliza correspondência exata de estação e horário, sem interpolação ou associação automática com horários próximos.

## 🛠️ Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| HTML5 | Estrutura das páginas. |
| CSS3 | Estilização e responsividade. |
| JavaScript | Interatividade e funcionalidades do site. |
| Python | Tratamento e integração dos dados. |
| Pandas | Manipulação de dados tabulares, quando utilizado pelo pipeline. |
| Chart.js | Construção dos gráficos do Dashboard. |
| JSON | Armazenamento dos dados resumidos utilizados pelo Dashboard. |
| CSV | Armazenamento dos dados de origem, tratados e integrados. |

## 📁 Estrutura do projeto

```text
stormwatchfiap/
│
├── index.html
├── README.md
├── requirements.txt
├── .gitignore
│
├── assets/
│   ├── css/
│   │   ├── dashboard.css
│   │   └── style.css
│   │
│   ├── img/
│   │   └── logotipo.png
│   │
│   └── js/
│       ├── dashboard.js
│       └── main.js
│
├── data/
│   ├── dashboard/
│   │   └── resumo.json
│   │
│   ├── raw/
│   │   ├── dados_geotecnicos.csv
│   │   ├── dados_hidrologicos.csv
│   │   └── dados_pluviometricos.csv
│   │
│   └── transformed/
│       ├── clean/
│       ├── integrated/
│       └── reports/
│
├── docs/
│   ├── dicionario_dados.md
│   ├── limitacoes_e_fontes.md
│   └── metodologia.md
│
├── includes/
│   ├── header.html
│   └── footer.html
│
├── pages/
│   ├── dashboard.html
│   ├── impacto.html
│   └── metodologia.html
│
└── scripts/
    └── preparar_dados.py
```

## ⚙️ Como executar o projeto

### 1. Pré-requisitos

Antes de iniciar, tenha instalado:

- Python 3.
- Visual Studio Code (recomendado).
- Extensão Live Server para o Visual Studio Code.

### 2. Clonar o repositório

```bash
git clone https://github.com/jheex/stormwatchfiap
```

Entre na pasta do projeto:

```bash
cd stormwatchfiap
```

### 3. Instalar as dependências Python

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente no Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

### 4. Executar o processamento dos dados

Na raiz do projeto, execute:

```bash
python scripts/preparar_dados.py
```

O script realiza o processamento dos arquivos de origem e gera os dados tratados, integrados e os arquivos utilizados pelo Dashboard.

### 5. Executar o site

Abra a pasta do projeto no Visual Studio Code.

Localize o arquivo `index.html`, clique com o botão direito e selecione:

**Open with Live Server**

O navegador abrirá o StormWatch.

> É importante executar o projeto por meio de um servidor local, pois o carregamento dos componentes HTML e dos dados JSON utiliza `fetch()`, que não funciona corretamente em determinadas situações quando os arquivos são abertos diretamente pelo navegador.

## 📚 Documentação

O projeto conta com documentos complementares para detalhar os processos e as informações utilizadas:

- `docs/metodologia.md`: apresenta a metodologia de tratamento e integração dos dados.
- `docs/dicionario_dados.md`: descreve os campos e as informações dos conjuntos de dados.
- `docs/limitacoes_e_fontes.md`: apresenta as fontes e limitações identificadas durante o desenvolvimento.

## ⚠️ Limitações e responsabilidade

O StormWatch é um projeto acadêmico de análise e visualização de dados ambientais.

É importante considerar que:

- Os dados disponíveis atualmente correspondem ao período de janeiro de 2026.
- O Dashboard apresenta informações históricas, não monitoramento em tempo real.
- A base utilizada não fornece todas as unidades de medida necessárias para interpretações físicas completas.
- Não foram disponibilizados limites oficiais de alerta para os sensores.
- Valores que exigem revisão são identificados e tratados com cautela, sem classificações arbitrárias.
- A proximidade geográfica entre estações não garante equivalência de condições ambientais.

**O StormWatch não substitui sistemas oficiais de monitoramento, previsão ou emissão de alertas.** As informações apresentadas têm finalidade de exploração, análise e conscientização.

Em situações de risco, a população deve acompanhar as orientações e os comunicados dos órgãos oficiais de defesa civil.

## 🌱 Impacto social

Acreditamos que a tecnologia deve ser utilizada para resolver problemas reais e melhorar a vida das pessoas.

O StormWatch busca contribuir para esse propósito ao tornar informações ambientais mais organizadas e acessíveis, incentivando a conscientização, a prevenção e a participação cidadã.

A iniciativa está alinhada ao conceito de **CitizenTech**, que coloca as necessidades da sociedade no centro do desenvolvimento tecnológico.

## 🚀 Possibilidades de evolução

O projeto possui possibilidades de expansão, como:

- Incorporação de novos períodos de dados.
- Ampliação das fontes de informações ambientais.
- Aprimoramento das visualizações e ferramentas de análise.
- Desenvolvimento de mecanismos de acompanhamento de tendências.
- Evolução das funcionalidades de acessibilidade.
- Estudos futuros sobre indicadores de risco, mediante disponibilidade de dados, validação técnica e critérios oficiais.

## 🎓 Sobre a Global Solution

Projeto desenvolvido para a **Global Solution — 2º Semestre de 2026**, da FIAP.

**Tema:** CitizenTech — Data Science, inovação e tecnologia colocando o cidadão no centro da inovação.

## 👥 Equipe e créditos

O StormWatch foi desenvolvido colaborativamente por:

- Jhonatan Lima Coelho
- João Torres de Brito
- Kewyn Montani Zancope
- Mariana Miyasaka Maruyama
- Thiago Rodrigues Pereira Santos

Projeto acadêmico desenvolvido no âmbito da Global Solution — 2º Semestre de 2026, da FIAP.

---

<p align="center">
  **StormWatch**
  <br>
  Tecnologia a serviço da sociedade.
  <br><br>
  🌧️ Prevenção · Informação · Segurança
</p>
