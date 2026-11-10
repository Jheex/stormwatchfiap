
/*
 * StormWatch — Dashboard
 * Consome data/dashboard/resumo.json, gerado pelo pipeline Python.
 * A base é histórica (janeiro de 2026), não é um monitoramento em tempo real.
 */

(() => {
  "use strict";

  const DATA_URL = "/data/dashboard/resumo.json";

  const COLORS = [
    "#00d8f0",
    "#168fe0",
    "#69c7ff",
    "#3475b8",
    "#8be8f4",
    "#4c9bd6",
    "#9cb9d0",
    "#1cbed0"
  ];

  const SOURCE_LABELS = {
    chuva: "Chuvas",
    hidrologia: "Hidrologia",
    geotecnia: "Geotecnia",
    todos: "Visão integrada"
  };

  const CHART_INFO = {
    chuva: [
      "Comportamento das chuvas",
      "registros pluviométricos"
    ],
    hidrologia: [
      "Comportamento hidrológico",
      "registros hidrológicos"
    ],
    geotecnia: [
      "Condições geotécnicas",
      "registros geotécnicos"
    ],
    todos: [
      "Panorama integrado",
      "registros das três fontes"
    ]
  };

  // Atalho para buscar elementos HTML pelo ID.
  const $ = id => document.getElementById(id);

  let dataset = null;
  let source = "chuva";
  let mainChart = null;
  let sensorChart = null;

  const numberFormat = new Intl.NumberFormat("pt-BR", {
    maximumFractionDigits: 2
  });

  const integerFormat = new Intl.NumberFormat("pt-BR");

  const formatNumber = value =>
    numberFormat.format(Number.isFinite(value) ? value : 0);

  const formatInteger = value =>
    integerFormat.format(Number.isFinite(value) ? value : 0);

  const formatDay = date =>
    `${date.slice(8, 10)}/${date.slice(5, 7)}`;

  // Identifica uma estação considerando sua fonte de dados.
  const stationKey = record =>
    `${record.source}|${record.station}`;

  const stationLabel = record =>
    `${record.station} — ${record.station_name}`;

  // Evita inserir conteúdo do JSON diretamente no HTML sem tratamento.
  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, character => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;"
    })[character]);
  }

  // Retorna os registros da fonte selecionada.
  function getSourceRecords() {
    return dataset.records.filter(record =>
      source === "todos" || record.source === source
    );
  }

  // Preenche um campo select sem perder uma opção ainda válida.
  function fillSelect(select, values, firstLabel) {
    const previous = select.value;

    const uniqueValues = [...new Set(values)]
      .sort((a, b) => a.localeCompare(b, "pt-BR"));

    select.innerHTML =
      `<option value="all">${firstLabel}</option>` +
      uniqueValues.map(value =>
        `<option value="${escapeHtml(value)}">${escapeHtml(value)}</option>`
      ).join("");

    select.value = uniqueValues.includes(previous)
      ? previous
      : "all";
  }

  // Atualiza os filtros conforme a fonte e as seleções anteriores.
  function updateFilterOptions() {
    const records = getSourceRecords();

    fillSelect(
      $("municipalityFilter"),
      records.map(record => record.municipality),
      "Todos os municípios"
    );

    const municipality = $("municipalityFilter").value;

    const municipalityRecords = records.filter(record =>
      municipality === "all" ||
      record.municipality === municipality
    );

    fillSelect(
      $("stationFilter"),
      municipalityRecords.map(stationLabel),
      "Todas as estações"
    );

    const station = $("stationFilter").value;

    const stationRecords = municipalityRecords.filter(record =>
      station === "all" ||
      stationLabel(record) === station
    );

    fillSelect(
      $("sensorFilter"),
      stationRecords.map(record => record.sensor),
      "Todos os sensores"
    );
  }

  // Aplica os filtros selecionados pelo usuário.
  function getFilteredRecords() {
    const municipality = $("municipalityFilter").value;
    const station = $("stationFilter").value;
    const sensor = $("sensorFilter").value;

    return getSourceRecords().filter(record =>
      (municipality === "all" ||
        record.municipality === municipality) &&

      (station === "all" ||
        stationLabel(record) === station) &&

      (sensor === "all" ||
        record.sensor === sensor)
    );
  }

  // Gera todas as datas do período analisado.
  function getDatesInPeriod() {
    const start = new Date(`${dataset.period.start}T12:00:00`);
    const end = new Date(`${dataset.period.end}T12:00:00`);

    const dates = [];

    for (
      const date = new Date(start);
      date <= end;
      date.setDate(date.getDate() + 1)
    ) {
      dates.push(
        `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`
      );
    }

    return dates;
  }

  // Agrupa os registros por dia.
  // A média é ponderada pela quantidade de registros originais.
  function aggregateDaily(records, metric) {
    const daily = new Map();

    records.forEach(record => {
      const group = daily.get(record.date) || {
        sum: 0,
        count: 0,
        max: -Infinity
      };

      group.sum += record.sum;
      group.count += record.count;
      group.max = Math.max(group.max, record.max);

      daily.set(record.date, group);
    });

    const dates = getDatesInPeriod();

    const values = dates.map(date => {
      const group = daily.get(date);

      if (!group) return 0;

      if (metric === "count") {
        return group.count;
      }

      if (metric === "max") {
        return group.max;
      }

      return group.count
        ? group.sum / group.count
        : 0;
    });

    return {
      labels: dates.map(formatDay),
      values
    };
  }

  // Atualiza os indicadores principais.
  function updateKpis(records) {
    const recordCount = records.reduce(
      (total, record) => total + record.count,
      0
    );

    const stations = new Set(
      records.map(stationKey)
    ).size;

    const municipalities = new Set(
      records.map(record => record.municipality)
    ).size;

    const days = new Set(
      records.map(record => record.date)
    ).size;

    $("kpiRecords").textContent =
      formatInteger(recordCount);

    $("kpiStations").textContent =
      formatInteger(stations);

    $("kpiCities").textContent =
      formatInteger(municipalities);

    $("kpiDays").textContent =
      formatInteger(days);

    $("kpiRecordsHint").textContent =
      `${SOURCE_LABELS[source]} · recorte atual`;
  }

  // Cria ou atualiza o gráfico temporal.
  function renderMainChart(records) {
    const selectedMetric = $("metricFilter").value;

    const metricLabels = {
      avg: "Média diária",
      max: "Máximo diário",
      count: "Quantidade diária"
    };

    // Na visão integrada, só comparamos quantidades de registros.
    const metric = source === "todos"
      ? "count"
      : selectedMetric;

    const aggregation = aggregateDaily(records, metric);

    const [title, description] = CHART_INFO[source];

    $("mainChartTitle").textContent = title;

    $("mainChartDescription").textContent =
      source === "todos"
        ? "Quantidade diária de registros somando as três fontes."
        : `${metricLabels[selectedMetric]} · ${description}.`;

    $("chartFootnote").textContent =
      source === "todos"
        ? "A visão integrada compara quantidades de registros; não soma nem mistura valores de grandezas físicas diferentes."
        : "As unidades de medida não foram informadas nos arquivos de origem. Os valores são apresentados sem atribuição de unidade.";

    if (mainChart) {
      mainChart.destroy();
    }

    mainChart = new Chart($("mainChart"), {
      type: "line",

      data: {
        labels: aggregation.labels,

        datasets: [{
          label:
            source === "todos" || metric === "count"
              ? "Registros"
              : metricLabels[metric],

          data: aggregation.values,

          borderColor: COLORS[0],
          backgroundColor: "rgba(0,216,240,.12)",
          borderWidth: 2.5,

          pointRadius:
            aggregation.values.length > 20 ? 0 : 3,

          pointHoverRadius: 5,
          fill: true,
          tension: 0.34
        }]
      },

      options: {
        responsive: true,
        maintainAspectRatio: false,

        animation: {
          duration: 700,
          easing: "easeOutQuart"
        },

        interaction: {
          intersect: false,
          mode: "index"
        },

        plugins: {
          legend: {
            display: false
          },

          tooltip: {
            backgroundColor: "#071a2c",
            borderColor: "rgba(0,216,240,.3)",
            borderWidth: 1,
            titleColor: "#eafaff",
            bodyColor: "#b9d5e7",

            callbacks: {
              label: context =>
                `${context.dataset.label}: ${formatNumber(context.parsed.y)}`
            }
          }
        },

        scales: {
          x: {
            grid: {
              color: "rgba(125,173,204,.08)"
            },

            ticks: {
              color: "#829db4",
              maxTicksLimit: 11
            }
          },

          y: {
            beginAtZero: true,

            grid: {
              color: "rgba(125,173,204,.1)"
            },

            ticks: {
              color: "#829db4",

              callback: value =>
                formatNumber(value)
            }
          }
        }
      }
    });
  }

  // Cria o gráfico de distribuição por sensor.
  function renderSensorChart(records) {
    const totals = new Map();

    records.forEach(record => {
      totals.set(
        record.sensor,
        (totals.get(record.sensor) || 0) + record.count
      );
    });

    const sorted = [...totals.entries()]
      .sort((a, b) => b[1] - a[1])
      .slice(0, 8);

    const total = sorted.reduce(
      (sum, item) => sum + item[1],
      0
    );

    if (sensorChart) {
      sensorChart.destroy();
    }

    sensorChart = new Chart($("sensorChart"), {
      type: "doughnut",

      data: {
        labels: sorted.map(item => item[0]),

        datasets: [{
          data: sorted.map(item => item[1]),

          backgroundColor: sorted.map(
            (_, index) => COLORS[index % COLORS.length]
          ),

          borderColor: "#0b2035",
          borderWidth: 3,
          hoverOffset: 8
        }]
      },

      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "67%",

        animation: {
          animateRotate: true,
          animateScale: true,
          duration: 700
        },

        plugins: {
          legend: {
            display: false
          },

          tooltip: {
            backgroundColor: "#071a2c",

            callbacks: {
              label: context =>
                `${context.label}: ${formatInteger(context.parsed)} registros`
            }
          }
        }
      }
    });

    // Legenda personalizada abaixo do gráfico.
    $("sensorLegend").innerHTML = sorted.length
      ? sorted.map(([name, count], index) =>
          `<div class="legend-row">
            <span class="legend-name">
              <i class="legend-swatch" style="background:${COLORS[index % COLORS.length]}"></i>
              ${escapeHtml(name)}
            </span>
            <b>${formatNumber(total ? count / total * 100 : 0)}%</b>
          </div>`
        ).join("")
      : "<p>Sem registros para os filtros selecionados.</p>";
  }

  // Monta a tabela de resumo por município.
  function renderTable(records) {
    const municipalities = new Map();

    records.forEach(record => {
      const group = municipalities.get(record.municipality) || {
        stations: new Set(),
        count: 0,
        sum: 0,
        max: -Infinity
      };

      group.stations.add(stationKey(record));
      group.count += record.count;
      group.sum += record.sum;
      group.max = Math.max(group.max, record.max);

      municipalities.set(record.municipality, group);
    });

    const rows = [...municipalities.entries()]
      .sort((a, b) => b[1].count - a[1].count)
      .slice(0, 12);

    $("municipalityTable").innerHTML = rows.length
      ? rows.map(([city, group]) => {

          // Não misturamos grandezas diferentes na visão integrada.
          const average = source === "todos"
            ? "Não comparável"
            : formatNumber(
                group.count ? group.sum / group.count : 0
              );

          const maximum = source === "todos"
            ? "Não comparável"
            : formatNumber(group.max);

          return `
            <tr>
              <td>${escapeHtml(city)}</td>
              <td>${formatInteger(group.stations.size)}</td>
              <td>${formatInteger(group.count)}</td>
              <td>${average}</td>
              <td>${maximum}</td>
            </tr>
          `;
        }).join("")
      : '<tr><td colspan="5">Nenhum registro encontrado para os filtros atuais.</td></tr>';
  }

  // Atualiza todos os componentes visuais.
  function render() {
    const records = getFilteredRecords();

    updateKpis(records);
    renderMainChart(records);
    renderSensorChart(records);
    renderTable(records);
  }

  // Alterna entre as fontes de monitoramento.
  function setSource(nextSource) {
    if (!Object.hasOwn(SOURCE_LABELS, nextSource)) {
      return;
    }

    source = nextSource;

    document.querySelectorAll(".source-tab").forEach(button => {
      const active = button.dataset.source === source;

      button.classList.toggle("active", active);

      button.setAttribute(
        "aria-selected",
        String(active)
      );
    });

    updateFilterOptions();
    render();
  }

  // Exibe o estado do carregamento da base.
  function updateStatus(message, isError = false) {
    const status = $("dataStatus");

    status.classList.toggle("error", isError);
    status.textContent = message;

    const indicator = document.createElement("i");
    status.prepend(indicator);
  }

  // Configura os eventos dos filtros e botões.
  function bindEvents() {

    // Abas das fontes de dados.
    document.querySelectorAll(".source-tab").forEach(button => {
      button.addEventListener("click", () => {
        setSource(button.dataset.source);
      });
    });

    // Filtro de município.
    $("municipalityFilter").addEventListener("change", () => {
      updateFilterOptions();
      render();
    });

    // Filtro de estação.
    $("stationFilter").addEventListener("change", () => {
      updateFilterOptions();
      render();
    });

    // Filtro de sensor.
    $("sensorFilter").addEventListener("change", render);

    // Filtro da métrica do gráfico.
    $("metricFilter").addEventListener("change", render);

    // Limpa todos os filtros.
    $("resetFilters").addEventListener("click", () => {
      $("municipalityFilter").value = "all";
      $("stationFilter").value = "all";
      $("sensorFilter").value = "all";
      $("metricFilter").value = "avg";

      updateFilterOptions();
      render();
    });
  }

  // Inicializa o dashboard após o carregamento do HTML.
  async function init() {
    const requiredIds = [
      "dataStatus",
      "municipalityFilter",
      "stationFilter",
      "sensorFilter",
      "metricFilter",
      "resetFilters",
      "kpiRecords",
      "kpiRecordsHint",
      "kpiStations",
      "kpiCities",
      "kpiDays",
      "mainChart",
      "mainChartTitle",
      "mainChartDescription",
      "chartFootnote",
      "sensorChart",
      "sensorLegend",
      "municipalityTable"
    ];

    // Verifica se os elementos necessários existem.
    const missing = requiredIds.filter(id => !$(id));

    if (missing.length) {
      console.error(
        "Elementos do dashboard não encontrados:",
        missing
      );
      return;
    }

    // Verifica se a biblioteca Chart.js foi carregada.
    if (!window.Chart) {
      updateStatus(
        "Biblioteca de gráficos indisponível",
        true
      );
      return;
    }

    try {
      // Busca o arquivo JSON com os dados processados.
      const response = await fetch(DATA_URL);

      if (!response.ok) {
        throw new Error(
          `Falha HTTP ${response.status} ao buscar ${DATA_URL}`
        );
      }

      dataset = await response.json();

      // Valida a estrutura básica do JSON.
      if (
        !Array.isArray(dataset.records) ||
        !dataset.period?.start ||
        !dataset.period?.end
      ) {
        throw new Error(
          "O JSON não possui a estrutura esperada (period e records)."
        );
      }

      // Atualiza o período exibido no cabeçalho.
      const start = new Date(
        `${dataset.period.start}T12:00:00`
      );

      const end = new Date(
        `${dataset.period.end}T12:00:00`
      );

      const periodLabel = date =>
        date.toLocaleDateString("pt-BR", {
          day: "2-digit",
          month: "short",
          year: "numeric"
        }).replace(" de ", " ").toUpperCase();

      const periodCard = document.querySelector(
        ".period-card strong"
      );

      if (periodCard) {
        periodCard.textContent =
          `${periodLabel(start)} — ${periodLabel(end)}`;
      }

      // Configura eventos e apresenta os dados iniciais.
      bindEvents();
      updateFilterOptions();
      render();

      updateStatus(
        `Base carregada · ${dataset.records.length.toLocaleString("pt-BR")} agregações`
      );

    } catch (error) {
      console.error(
        "Falha ao carregar os dados do dashboard:",
        error
      );

      updateStatus(
        "Não foi possível carregar a base",
        true
      );

      $("municipalityTable").innerHTML =
        '<tr><td colspan="5">Verifique se data/dashboard/resumo.json existe e abra o site por um servidor local, como o Live Server do VS Code.</td></tr>';

      [
        "kpiRecords",
        "kpiStations",
        "kpiCities",
        "kpiDays"
      ].forEach(id => {
        if ($(id)) {
          $(id).textContent = "—";
        }
      });
    }
  }

  // Executa a inicialização quando o documento estiver pronto.
  document.addEventListener("DOMContentLoaded", init);

})();
