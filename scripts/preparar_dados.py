#!/usr/bin/env python3

"""Limpeza, validação e integração das bases CSV do StormWatch.
Dependências: somente biblioteca padrão do Python 3.10+.
Preserva os CSVs originais e grava os resultados em data/transformed/.
"""

from __future__ import annotations
import argparse
import csv
import json
import math
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

# Os CSVs fornecidos usam ponto e vírgula como separador.
CSV_DELIMITER = ";"

# Código especial observado nos sensores de umidade do solo. Não representa
# uma medição física: no dado tratado vira ausência, mas o original é guardado.
SENTINEL_GEOTECH = -1000.0

# Valor recorrente em leituras de nível hidrológico. É sinalizado para
# conferência, mas não descartado porque falta documentação do sensor.
SUSPECT_HYDRO_LEVEL = 35.0

# Relação entre o nome lógico da base e o nome do CSV bruto esperado.
# O script espera estes três arquivos dentro da pasta de entrada.
FILES = {
    "pluviometrica": "dados_pluviometricos.csv",
    "geotecnica": "dados_geotecnicos.csv",
    "hidrologica": "dados_hidrologicos.csv",
}

# Define, explicitamente, as colunas e a ordem dos CSVs limpos.
# valorMedida_original preserva o conteúdo recebido; valorMedida contém
# a versão numérica normalizada e, quando aplicável, tratada.
CLEAN_FIELDS = {
    "pluviometrica": [
        "municipio", "codEstacao", "uf", "nomeEstacao", "latitude", "longitude",
        "datahora", "valorMedida", "valorMedida_original", "status_qualidade", "origem",
    ],

    "geotecnica": [
        "municipio", "codEstacao", "uf", "nomeEstacao", "latitude", "longitude",
        "datahora", "sensor", "valorMedida", "valorMedida_original", "status_qualidade", "origem",
    ],

    "hidrologica": [
        "municipio", "codEstacao", "uf", "nomeEstacao", "latitude", "longitude", "offset",
        "datahora", "sensor", "valorMedida", "valorMedida_original", "status_qualidade", "origem",
    ],
}

def parse_number(raw: Any) -> float | None:
    """Converte um valor textual em número.
    Aceita tanto decimal brasileiro (1.234,56) quanto decimal com ponto
    (1234.56). Retorna None quando o campo está vazio, inválido ou infinito.
    """
    if raw is None:
        return None
    value = str(raw).strip()

    if not value:
        return None

    value = value.replace("\u00a0", "").replace(" ", "")
    if "," in value:
        value = value.replace(".", "").replace(",", ".")

    try:
        number = float(value)

    except ValueError:
        return None
    return number if math.isfinite(number) else None

def parse_datetime(raw: Any) -> str | None:
    """Normaliza uma data ISO para AAAA-MM-DD HH:MM:SS.

    Não atribui fuso horário: os arquivos de origem não informam essa
    informação, portanto inventá-la poderia deslocar as observações.
    """

    if raw is None or not str(raw).strip():
        return None
    value = str(raw).strip()

    try:
        parsed = datetime.fromisoformat(value.replace(" ", "T"))
        # Os arquivos de origem não trazem fuso horário. Não inventamos um.
        return parsed.strftime("%Y-%m-%d %H:%M:%S")

    except ValueError:
        return None

def fmt_number(value: float | None) -> str:
    """Formata números de forma compacta para gravar nos CSVs."""
    if value is None:
        return ""
    return format(value, ".12g")


def add_status(parts: list[str], status: str) -> None:
    """Adiciona uma ocorrência de qualidade sem repetir o mesmo rótulo."""
    if status not in parts:
        parts.append(status)

def station_metadata(row: dict[str, str]) -> dict[str, Any]:
    """Extrai os metadados de identificação e localização de uma estação."""

    return {
        "municipio": (row.get("municipio") or "").strip(),
        "codEstacao": (row.get("codEstacao") or "").strip(),
        "uf": (row.get("uf") or "").strip(),
        "nomeEstacao": (row.get("nomeEstacao") or "").strip(),
        "latitude": parse_number(row.get("latitude")),
        "longitude": parse_number(row.get("longitude")),
    }

def valid_coordinates(lat: float | None, lon: float | None) -> bool:
    """Verifica se latitude e longitude estão dentro dos limites terrestres."""
    return lat is not None and lon is not None and -90 <= lat <= 90 and -180 <= lon <= 180

def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calcula a distância aproximada entre duas coordenadas, em metros.
    A fórmula de Haversine considera a curvatura da Terra e é usada aqui
    para encontrar a estação pluviométrica geograficamente mais próxima.
    """
    radius = 6_371_000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * radius * math.asin(math.sqrt(a))

def write_csv(path: Path, fields: list[str], rows) -> int:
    """Grava um CSV padronizado e devolve a quantidade de linhas escritas.
    utf-8-sig facilita a abertura dos arquivos no Excel. O separador é
    ponto e vírgula, conforme o padrão das bases recebidas.
    """

    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter=CSV_DELIMITER, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
            count += 1
    return count

# Consolida estações de diferentes bases em um catálogo comum.
# Se o mesmo código vier com metadados divergentes, registra o conflito
# em vez de escolher silenciosamente qual informação é correta.
def register_station(all_stations: dict[str, dict[str, Any]], row: dict[str, str], source: str,
                     conflicts: list[dict[str, Any]]) -> None:
    meta = station_metadata(row)
    code = meta["codEstacao"]

    if not code:
        return

    if code not in all_stations:
        all_stations[code] = {
            **meta, "origens": set(), "quantidade_registros": 0,
            "quantidade_pluviometrica": 0, "quantidade_geotecnica": 0,
            "quantidade_hidrologica": 0,
        }

    current = all_stations[code]
    for field in ("municipio", "nomeEstacao", "uf", "latitude", "longitude"):
        old, new = current.get(field), meta.get(field)
        if old not in (None, "") and new not in (None, "") and old != new:
            conflicts.append({"codEstacao": code, "campo": field, "valor_catalogo": old, "valor_observado": new, "origem": source})
        elif old in (None, "") and new not in (None, ""):
            current[field] = new
    current["origens"].add(source)
    current["quantidade_registros"] += 1
    current[f"quantidade_{source}"] += 1

# Processa uma base por vez. Além de escrever o CSV limpo, devolve estruturas
# em memória que serão usadas para cruzar as observações sem reler os arquivos.
def clean_one(source: str, input_path: Path, output_path: Path,
              all_stations: dict[str, dict[str, Any]], conflicts: list[dict[str, Any]]):
    if not input_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {input_path}")
    # Estruturas de acumulação: estatísticas, chaves já vistas e dados
    # organizados por estação/horário para permitir os cruzamentos posteriores.
    stats: dict[str, Any] = {
        "arquivo": input_path.name, "registros": 0, "estacoes": set(), "municipios": set(),
        "sensores": Counter(), "status_qualidade": Counter(), "valores_por_sensor": defaultdict(lambda: {"quantidade": 0, "min": None, "max": None}),
        "datas": [], "chaves_duplicadas": 0, "campos_ausentes": Counter(),
        "valores_numericos_invalidos": 0, "datas_invalidas": 0, "coordenadas_invalidas": 0,
        "sentinela_menos_1000": 0, "nivel_35_suspeito": 0,
    }

    seen: set[tuple[str, ...]] = set()
    pluv_rows: dict[tuple[str, str], float | None] = {}
    pivot: dict[tuple[str, str], dict[str, float | None]] = {}
    pivot_meta: dict[str, dict[str, Any]] = {}

    # A base pluviométrica possui uma leitura por estação e horário.
    # As outras duas também distinguem o sensor na chave de unicidade.
    if source == "pluviometrica":
        key_fields = ("codEstacao", "datahora")
    else:
        key_fields = ("codEstacao", "datahora", "sensor")

    with input_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=CSV_DELIMITER)
        expected = set(CLEAN_FIELDS[source]) - {"valorMedida_original", "status_qualidade", "origem"}
        if source == "pluviometrica":
            expected.discard("sensor")
        missing_headers = sorted(expected - set(reader.fieldnames or []))

        if missing_headers:
            raise ValueError(f"Colunas ausentes em {input_path.name}: {missing_headers}")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8-sig", newline="") as out_handle:
            writer = csv.DictWriter(out_handle, fieldnames=CLEAN_FIELDS[source], delimiter=CSV_DELIMITER)
            writer.writeheader()

            for row in reader:
                stats["registros"] += 1
                for field, value in row.items():
                    if value is None or not value.strip():
                        stats["campos_ausentes"][field] += 1

                meta = station_metadata(row)
                code = meta["codEstacao"]
                if code:
                    stats["estacoes"].add(code)
                if meta["municipio"]:
                    stats["municipios"].add(meta["municipio"])
                register_station(all_stations, row, source, conflicts)

                sensor = (row.get("sensor") or "pluviometria").strip() or "pluviometria"
                stats["sensores"][sensor] += 1
                dt = parse_datetime(row.get("datahora"))
                raw_value = row.get("valorMedida")
                value = parse_number(raw_value)
                lat, lon = meta["latitude"], meta["longitude"]
                status: list[str] = []

                if dt is None:
                    stats["datas_invalidas"] += 1
                    add_status(status, "datahora_invalida")
                else:
                    stats["datas"].append(dt)
                if not valid_coordinates(lat, lon):
                    stats["coordenadas_invalidas"] += 1
                    add_status(status, "coordenada_invalida")
                if raw_value is None or not str(raw_value).strip():
                    add_status(status, "valor_ausente")
                elif value is None:
                    stats["valores_numericos_invalidos"] += 1
                    add_status(status, "valor_numerico_invalido")

                # Regra de tratamento: -1000 é um código sentinela observado
                # nos sensores de umidade. O valor original continua preservado
                # em valorMedida_original; apenas o campo analítico vira vazio.
                # Isso evita que -1000 distorça médias, mínimos e gráficos.
                if source == "geotecnica" and sensor.startswith("umidade_solo") and value == SENTINEL_GEOTECH:
                    stats["sentinela_menos_1000"] += 1
                    value = None
                    add_status(status, "sentinela_-1000_convertida_em_ausente")

                # Não descartamos o valor 35. Apenas o marcamos para revisão,
                # pois pode representar um limite do equipamento, mas isso ainda
                # depende de confirmação na documentação técnica do sensor.

                if source == "hidrologica" and sensor.casefold() in ("nível", "nivel") and value == SUSPECT_HYDRO_LEVEL:
                    stats["nivel_35_suspeito"] += 1
                    add_status(status, "revisar_nivel_35_possivel_limite_sensor")

                if source in ("pluviometrica", "geotecnica") and sensor in ("chuva", "pluviometria") and value is not None and value < 0:
                    add_status(status, "precipitacao_negativa_revisar")

                # Verifica duplicidade pela chave natural definida para cada base.
                # Registros repetidos são preservados no CSV, mas ficam sinalizados.
                key = tuple((code if field == "codEstacao" else dt if field == "datahora" else (row.get(field) or "").strip()) for field in key_fields)

                if all(key) and key in seen:
                    stats["chaves_duplicadas"] += 1
                    add_status(status, "chave_duplicada_preservada")
                elif all(key):
                    seen.add(key)

                stats["status_qualidade"][";".join(status) if status else "ok"] += 1
                vstats = stats["valores_por_sensor"][sensor]
                if value is not None:
                    vstats["quantidade"] += 1
                    vstats["min"] = value if vstats["min"] is None else min(vstats["min"], value)
                    vstats["max"] = value if vstats["max"] is None else max(vstats["max"], value)

                out = {
                    "municipio": meta["municipio"], "codEstacao": code, "uf": meta["uf"],
                    "nomeEstacao": meta["nomeEstacao"], "latitude": fmt_number(lat),
                    "longitude": fmt_number(lon), "datahora": dt or "",
                    "valorMedida": fmt_number(value), "valorMedida_original": raw_value or "",
                    "status_qualidade": ";".join(status) if status else "ok", "origem": input_path.name,
                }

                if source == "geotecnica":
                    out["sensor"] = sensor
                elif source == "hidrologica":
                    out["sensor"] = sensor
                    out["offset"] = fmt_number(parse_number(row.get("offset")))
                writer.writerow(out)

                if dt is not None and code:
                    if source == "pluviometrica":
                        pluv_rows.setdefault((code, dt), value)
                    else:
                        key2 = (code, dt)
                        pivot.setdefault(key2, {})
                        # Em chave repetida, conservamos a primeira leitura para não
                        # multiplicar observações silenciosamente na integração.
                        pivot[key2].setdefault(sensor, value)
                        pivot_meta.setdefault(code, meta)

    # JSON-friendly conversion, keeping detailed sensor stats.
    stats_out = {
        "arquivo": stats["arquivo"], "registros": stats["registros"],
        "estacoes": len(stats["estacoes"]), "municipios": len(stats["municipios"]),
        "sensores": dict(stats["sensores"]), "status_qualidade": dict(stats["status_qualidade"]),
        "valores_por_sensor": stats["valores_por_sensor"],
        "periodo": {"inicio": min(stats["datas"]) if stats["datas"] else None,
                    "fim": max(stats["datas"]) if stats["datas"] else None},
        "chaves_duplicadas": stats["chaves_duplicadas"],
        "campos_ausentes": dict(stats["campos_ausentes"]),
        "valores_numericos_invalidos": stats["valores_numericos_invalidos"],
        "datas_invalidas": stats["datas_invalidas"],
        "coordenadas_invalidas": stats["coordenadas_invalidas"],
        "sentinela_menos_1000_convertida_em_ausente": stats["sentinela_menos_1000"],
        "nivel_35_sinalizado_para_revisao": stats["nivel_35_suspeito"],
    }

    return stats_out, pluv_rows, pivot, pivot_meta

# Para cada estação geotécnica/hidrológica, procura a estação pluviométrica
# mais próxima. Distâncias até 1 metro são tratadas como correspondência exata;
# acima disso, a relação é apenas candidata e requer validação humana.
def station_matches(source_stations: dict[str, dict[str, Any]], pluv_stations: dict[str, dict[str, Any]], source_name: str):
    pluv_valid = [(code, data) for code, data in pluv_stations.items()
                  if valid_coordinates(data.get("latitude"), data.get("longitude"))]
    results: dict[str, dict[str, Any]] = {}
    rows = []
    for code, station in sorted(source_stations.items()):
        lat, lon = station.get("latitude"), station.get("longitude")
        nearest = None
        if valid_coordinates(lat, lon) and pluv_valid:
            distances = [
                (haversine_m(lat, lon, pdata["latitude"], pdata["longitude"]), pcode, pdata)
                for pcode, pdata in pluv_valid
            ]
            nearest = min(distances, key=lambda item: item[0])
        if nearest is None:
            pcode, pdata, distance, match_type = "", {}, None, "sem_coordenada_comparavel"
        else:
            distance, pcode, pdata = nearest
            match_type = "exata" if distance <= 1.0 else "aproximada_candidata_requer_validacao"
        results[code] = {
            "cod_pluviometrica": pcode,
            "distancia_m": distance,
            "tipo": match_type,
        }

        rows.append({
            "tipo_estacao_origem": source_name, "cod_estacao_origem": code,
            "municipio": station.get("municipio", ""), "nome_estacao_origem": station.get("nomeEstacao", ""),
            "latitude": fmt_number(lat), "longitude": fmt_number(lon),
            "cod_estacao_pluviometrica_candidata": pcode,
            "nome_estacao_pluviometrica": pdata.get("nomeEstacao", ""),
            "municipio_pluviometrico": pdata.get("municipio", ""),
            "distancia_m": fmt_number(distance), "tipo_correspondencia": match_type,
        })
    return results, rows

# Monta tabelas largas (uma linha por estação/horário), aproximando chuva
# e medições ambientais somente quando estação e timestamp coincidem.
# Não interpola horários nem procura a leitura temporalmente mais próxima.
def build_integrations(integrated_dir: Path, all_stations: dict[str, dict[str, Any]],
                       pluv_rows: dict[tuple[str, str], float | None],
                       hydro_pivot: dict[tuple[str, str], dict[str, float | None]],
                       hydro_meta: dict[str, dict[str, Any]],
                       geo_pivot: dict[tuple[str, str], dict[str, float | None]],
                       geo_meta: dict[str, dict[str, Any]],
                       hydro_matches: dict[str, dict[str, Any]], geo_matches: dict[str, dict[str, Any]]):
    pluv_stations = {c: s for c, s in all_stations.items() if s["quantidade_pluviometrica"] > 0}

    hydro_fields = [
        "cod_estacao_hidrologica", "municipio", "nome_estacao", "latitude", "longitude", "datahora",
        "nivel_hidrologico", "status_nivel", "chuva_hidrologica", "chuva_pluviometrica",
        "cod_estacao_pluviometrica", "correspondencia_pluviometrica", "distancia_pluviometrica_m",
    ]

    hydro_integrated = []
    hydro_by_station_times: dict[str, set[str]] = defaultdict(set)

    for code, dt in hydro_pivot:
        hydro_by_station_times[code].add(dt)
    for hcode, match in hydro_matches.items():
        pcode = match["cod_pluviometrica"]
        times = set(hydro_by_station_times.get(hcode, set()))
        if pcode:
            times.update(dt for (pc, dt) in pluv_rows if pc == pcode)
        station = hydro_meta.get(hcode, {})

        for dt in sorted(times):
            metrics = hydro_pivot.get((hcode, dt), {})
            level = metrics.get("nível", metrics.get("nivel"))
            rain_h = metrics.get("chuva")
            level_status = "revisar_valor_35" if level == SUSPECT_HYDRO_LEVEL else ("sem_leitura_neste_horario" if level is None else "ok")
            hydro_integrated.append({
                "cod_estacao_hidrologica": hcode, "municipio": station.get("municipio", ""),
                "nome_estacao": station.get("nomeEstacao", ""), "latitude": fmt_number(station.get("latitude")),
                "longitude": fmt_number(station.get("longitude")), "datahora": dt,
                "nivel_hidrologico": fmt_number(level), "status_nivel": level_status,
                "chuva_hidrologica": fmt_number(rain_h),
                "chuva_pluviometrica": fmt_number(pluv_rows.get((pcode, dt))) if pcode else "",
                "cod_estacao_pluviometrica": pcode,
                "correspondencia_pluviometrica": match["tipo"],
                "distancia_pluviometrica_m": fmt_number(match["distancia_m"]),
            })
    write_csv(integrated_dir / "integracao_hidrologico_pluviometrico.csv", hydro_fields, hydro_integrated)

    geo_fields = [
        "cod_estacao_geotecnica", "municipio", "nome_estacao", "latitude", "longitude", "datahora",
        "umidade_solo_nivel1", "umidade_solo_nivel2", "umidade_solo_nivel3",
        "umidade_solo_nivel4", "umidade_solo_nivel5", "umidade_solo_nivel6",
        "chuva_geotecnica", "chuva_pluviometrica", "cod_estacao_pluviometrica_candidata",
        "correspondencia_pluviometrica", "distancia_pluviometrica_m", "quantidade_niveis_umidade_validos",
    ]

    geo_integrated = []
    moisture_sensors = [f"umidade_solo_nivel{i}" for i in range(1, 7)]
    for (gcode, dt), metrics in sorted(geo_pivot.items()):
        match = geo_matches.get(gcode, {})
        pcode = match.get("cod_pluviometrica", "")
        station = geo_meta.get(gcode, {})
        moisture = [metrics.get(sensor) for sensor in moisture_sensors]
        geo_integrated.append({
            "cod_estacao_geotecnica": gcode, "municipio": station.get("municipio", ""),
            "nome_estacao": station.get("nomeEstacao", ""), "latitude": fmt_number(station.get("latitude")),
            "longitude": fmt_number(station.get("longitude")), "datahora": dt,
            **{sensor: fmt_number(metrics.get(sensor)) for sensor in moisture_sensors},
            "chuva_geotecnica": fmt_number(metrics.get("chuva")),
            "chuva_pluviometrica": fmt_number(pluv_rows.get((pcode, dt))) if pcode else "",
            "cod_estacao_pluviometrica_candidata": pcode,
            "correspondencia_pluviometrica": match.get("tipo", "sem_correspondencia"),
            "distancia_pluviometrica_m": fmt_number(match.get("distancia_m")),
            "quantidade_niveis_umidade_validos": sum(v is not None for v in moisture),
        })
    write_csv(integrated_dir / "integracao_geotecnico_pluviometrico.csv", geo_fields, geo_integrated)

    # Catálogo único de estações para mapas e filtros do frontend.
    # A contagem por origem permite saber quais sensores existem em cada estação.
    catalog_fields = [
        "codEstacao", "municipio", "uf", "nomeEstacao", "latitude", "longitude", "origens",
        "quantidade_registros", "quantidade_pluviometrica", "quantidade_geotecnica", "quantidade_hidrologica",
    ]

    catalog_rows = []
    for code, s in sorted(all_stations.items()):
        catalog_rows.append({
            "codEstacao": code, "municipio": s.get("municipio", ""), "uf": s.get("uf", ""),
            "nomeEstacao": s.get("nomeEstacao", ""), "latitude": fmt_number(s.get("latitude")),
            "longitude": fmt_number(s.get("longitude")), "origens": ";".join(sorted(s["origens"])),
            "quantidade_registros": s["quantidade_registros"],
            "quantidade_pluviometrica": s["quantidade_pluviometrica"],
            "quantidade_geotecnica": s["quantidade_geotecnica"],
            "quantidade_hidrologica": s["quantidade_hidrologica"],
        })

    write_csv(integrated_dir / "catalogo_estacoes.csv", catalog_fields, catalog_rows)
    return {
        "linhas_integracao_hidrologico_pluviometrico": len(hydro_integrated),
        "linhas_integracao_geotecnico_pluviometrico": len(geo_integrated),
        "estacoes_catalogadas": len(catalog_rows),
    }

def json_safe(value):
    """Converte tipos especiais (set, Counter etc.) para tipos aceitos pelo JSON."""
    if isinstance(value, set):
        return sorted(value)
    if isinstance(value, Counter):
        return dict(value)
    if isinstance(value, defaultdict):
        return dict(value)
    if isinstance(value, datetime):
        return value.isoformat(sep=" ")
    raise TypeError(f"Tipo não serializável: {type(value).__name__}")

def main() -> int:
    """Coordena o pipeline completo e define pastas/arquivos de entrada e saída."""
    script_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Prepara e integra os CSVs do StormWatch.")

    # Caminhos padrão relativos à raiz do projeto. Podem ser substituídos
    # pelos parâmetros --input-dir e --output-dir na linha de comando.
    parser.add_argument("--input-dir", type=Path, default=script_root / "data" / "raw",
                        help="Pasta com os três CSVs originais (padrão: ./data/raw).")
    parser.add_argument("--output-dir", type=Path, default=script_root / "data" / "transformed",
                        help="Raiz de saída (padrão: ./data/transformed).")
    
    args = parser.parse_args()
    output_dir: Path = args.output_dir
    clean_dir = output_dir / "clean"
    integrated_dir = output_dir / "integrated"
    reports_dir = output_dir / "reports"

    for folder in (clean_dir, integrated_dir, reports_dir):
        folder.mkdir(parents=True, exist_ok=True)

    all_stations: dict[str, dict[str, Any]] = {}
    metadata_conflicts: list[dict[str, Any]] = []
    file_stats: dict[str, Any] = {}
    pluv_rows = {}
    geo_pivot = {}
    geo_meta = {}
    hydro_pivot = {}
    hydro_meta = {}

    # Etapa 1: normalização e validação individual das três bases.
    print("[1/5] Limpando e validando CSVs...")
    for source in ("pluviometrica", "geotecnica", "hidrologica"):
        input_path = args.input_dir / FILES[source]
        output_names = {
            "pluviometrica": "dados_pluviometricos_limpos.csv",
            "geotecnica": "dados_geotecnicos_limpos.csv",
            "hidrologica": "dados_hidrologicos_limpos.csv",
        }

        output_path = clean_dir / output_names[source]
        stats, readings, pivot, pivot_meta = clean_one(source, input_path, output_path, all_stations, metadata_conflicts)
        file_stats[source] = stats
        if source == "pluviometrica":
            pluv_rows = readings
        elif source == "geotecnica":
            geo_pivot, geo_meta = pivot, pivot_meta
        else:
            hydro_pivot, hydro_meta = pivot, pivot_meta
        print(f"  - {FILES[source]}: {stats['registros']:,} linhas; {stats['estacoes']} estações")

    pluv_stations = {code: s for code, s in all_stations.items() if s["quantidade_pluviometrica"] > 0}
    geo_stations = {code: s for code, s in all_stations.items() if s["quantidade_geotecnica"] > 0}
    hydro_stations = {code: s for code, s in all_stations.items() if s["quantidade_hidrologica"] > 0}

    # Etapa 2: correspondência espacial pela distância entre coordenadas.
    print("[2/5] Cruzando estações por coordenadas...")
    geo_matches, geo_match_rows = station_matches(geo_stations, pluv_stations, "geotecnica")
    hydro_matches, hydro_match_rows = station_matches(hydro_stations, pluv_stations, "hidrologica")
    match_fields = [
        "tipo_estacao_origem", "cod_estacao_origem", "municipio", "nome_estacao_origem", "latitude", "longitude",
        "cod_estacao_pluviometrica_candidata", "nome_estacao_pluviometrica", "municipio_pluviometrico",
        "distancia_m", "tipo_correspondencia",
    ]
    write_csv(integrated_dir / "correspondencia_estacoes.csv", match_fields, geo_match_rows + hydro_match_rows)

    # Etapa 3: integração por estação e data/hora exatas.
    print("[3/5] Construindo integrações temporais...")
    integration_stats = build_integrations(integrated_dir, all_stations, pluv_rows, hydro_pivot, hydro_meta,
                                           geo_pivot, geo_meta, hydro_matches, geo_matches)

    # Etapa 4: reúne métricas, avisos e contagens em um relatório JSON.
    print("[4/5] Gerando relatório de qualidade...")
    def counts(matches):
        return {
            "estacoes_origem": len(matches),
            "correspondencias_exatas": sum(1 for m in matches.values() if m["tipo"] == "exata"),
            "candidatas_aproximadas": sum(1 for m in matches.values() if m["tipo"] == "aproximada_candidata_requer_validacao"),
        }

    report = {
        "projeto": "StormWatch",
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "observacao_fuso": "Os horários foram preservados como recebidos; os CSVs não informam fuso horário.",
        "formato_saida": "CSV UTF-8 com BOM, separador ponto e vírgula; números com ponto decimal.",
        "regras_aplicadas": [
            "Os CSVs originais não são alterados.",
            "Valores -1000 nos sensores de umidade do solo são convertidos em ausentes no campo valorMedida; o original permanece em valorMedida_original.",
            "Nível hidrológico igual a 35 é preservado, mas sinalizado para revisão por possível limite/saturação do sensor.",
            "Valores 35 em sensores de umidade do solo são preservados; não há evidência suficiente para classificá-los como inválidos.",
            "As integrações temporais usam correspondência exata de estação (ou estação pluviométrica próxima candidata no caso geotécnico) e datahora; não há interpolação.",
            "Correspondências geográficas acima de 1 metro são identificadas como aproximadas e devem ser validadas antes de inferências.",
            "Não são aplicados limites físicos de alerta porque a documentação das unidades e dos limiares oficiais não foi fornecida.",
        ],

        "arquivos": file_stats,
        "correspondencias_estacoes": {
            "geotecnica_com_pluviometrica": counts(geo_matches),
            "hidrologica_com_pluviometrica": counts(hydro_matches),
        },

        "integracoes": integration_stats,
        "conflitos_metadados_cod_estacao": metadata_conflicts,
    }

    report_path = reports_dir / "relatorio_qualidade.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=json_safe), encoding="utf-8")

    
    # Etapa 5: gera a base agregada consumida pelo dashboard.
    print("[5/6] Gerando dados dinâmicos do dashboard...")

    dashboard_dir = output_dir.parent / "dashboard"

    dashboard_path = generate_dashboard_json(
        clean_dir,
        dashboard_dir,
        file_stats,
    )

    print(f"Dashboard JSON: {dashboard_path}")

    # Etapa 6: informa os caminhos finais.
    print("[6/6] Concluído.")
    print(f"Dados limpos: {clean_dir}")
    print(f"Integrações: {integrated_dir}")
    print(f"Relatórios: {reports_dir}")
    print(f"Correspondências geotécnicas: {counts(geo_matches)}")
    print(f"Correspondências hidrológicas: {counts(hydro_matches)}")
    print(f"Relatório: {report_path}")
    print(f"Dados do dashboard: {dashboard_path}")
    print(f"Registros agregados: {len(json.loads(dashboard_path.read_text(encoding='utf-8'))['records']):,}")

def generate_dashboard_json(clean_dir: Path, dashboard_dir: Path, file_stats: dict[str, Any]) -> Path:
    """
    Lê os CSVs limpos e gera as agregações utilizadas pelo dashboard.
    Cada registro do JSON representa uma combinação de: origem + data + município + estação + sensor.
    As estatísticas são calculadas somente com valores numéricos válidos.
    """

    input_files = {
        "chuva": clean_dir / "dados_pluviometricos_limpos.csv",
        "geotecnia": clean_dir / "dados_geotecnicos_limpos.csv",
        "hidrologia": clean_dir / "dados_hidrologicos_limpos.csv",
    }

    # Chave: origem, data, município, estação, nome da estação e sensor.
    aggregates = {}

    for source, input_path in input_files.items():
        if not input_path.exists():
            raise FileNotFoundError(
                f"CSV limpo não encontrado para o dashboard: {input_path}"
            )

        with input_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, delimiter=CSV_DELIMITER)

            for row in reader:
                date = (row.get("datahora") or "").strip()[:10]
                municipality = (row.get("municipio") or "").strip()
                station = (row.get("codEstacao") or "").strip()
                station_name = (row.get("nomeEstacao") or "").strip()

                # O CSV pluviométrico não possui coluna sensor.
                sensor = (
                    (row.get("sensor") or "").strip()
                    if source != "chuva"
                    else "precipitacao"
                )

                value = parse_number(row.get("valorMedida"))

                # Sem data, município ou estação, o registro não pode
                # participar dos agrupamentos utilizados pelos filtros.
                if not date or not municipality or not station:
                    continue

                key = (
                    source,
                    date,
                    municipality,
                    station,
                    station_name,
                    sensor,
                )

                if key not in aggregates:
                    aggregates[key] = {
                        "count": 0,
                        "sum": 0.0,
                        "min": None,
                        "max": None,
                    }

                # Registros sem valor numérico não entram nas estatísticas.
                # Eles continuam contabilizados no relatório de qualidade.
                if value is None:
                    continue
                item = aggregates[key]
                item["count"] += 1
                item["sum"] += value
                item["min"] = value if item["min"] is None else min(item["min"], value)
                item["max"] = value if item["max"] is None else max(item["max"], value)

    records = []

    for key, metrics in aggregates.items():
        source, date, municipality, station, station_name, sensor = key

        # Grupos sem medições válidas não geram pontos nos gráficos.
        if metrics["count"] == 0:
            continue
        records.append({
            "source": source,
            "date": date,
            "municipality": municipality,
            "station": station,
            "station_name": station_name,
            "sensor": sensor,
            "count": metrics["count"],
            "sum": round(metrics["sum"], 10),
            "avg": round(metrics["sum"] / metrics["count"], 10),
            "min": metrics["min"],
            "max": metrics["max"],
        })

    records.sort(
        key=lambda item: (
            item["source"],
            item["date"],
            item["municipality"],
            item["station"],
            item["sensor"],
        )
    )

    source_metadata = {}

    source_mapping = {
        "chuva": "pluviometrica",
        "geotecnia": "geotecnica",
        "hidrologia": "hidrologica",
    }

    for dashboard_source, original_source in source_mapping.items():
        stats = file_stats[original_source]

        source_metadata[dashboard_source] = {
            "records_source": stats["registros"],
            "stations": stats["estacoes"],
            "municipalities": stats["municipios"],
        }

    dates = [record["date"] for record in records]

    dashboard_data = {
        "period": {
            "start": min(dates) if dates else None,
            "end": max(dates) if dates else None,
        },
        "source_metadata": source_metadata,
        "total_records": sum(
            stats["registros"] for stats in file_stats.values()
        ),
        "aggregated_records": len(records),
        "records": records,
    }

    dashboard_dir.mkdir(parents=True, exist_ok=True)
    output_path = dashboard_dir / "resumo.json"
    output_path.write_text(
        json.dumps(
            dashboard_data,
            ensure_ascii=False,
            separators=(",", ":"),
        ),
        encoding="utf-8",
    )

    return output_path

if __name__ == "__main__":
    try:
        raise SystemExit(main())

    except Exception as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        raise