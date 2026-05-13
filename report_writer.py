"""
report_writer.py
----------------
Módulo de escritura de reportes. Genera archivos .txt y .html
a partir de un DataSummary producido por el módulo analyzer.
"""

from datetime import datetime

from analyzer import DataSummary, ColumnSummary
from logger import get_logger

logger = get_logger(__name__)


# ──────────────────────────────────────────────
# Reporte TXT
# ──────────────────────────────────────────────

def _txt_separator(char: str = "─", width: int = 60) -> str:
    return char * width


def _txt_column_block(col: ColumnSummary) -> str:
    """Formatea el bloque de texto para una columna."""
    lines = [
        f"  Columna : {col.name}",
        f"  Tipo    : {col.dtype}",
        f"  Nulos   : {col.null_count} ({col.null_pct}%)",
        f"  Únicos  : {col.unique_count}",
    ]
    if col.stats:
        lines.append("  Estadísticas:")
        for k, v in col.stats.items():
            lines.append(f"    {k:<8}: {v}")
    if col.top_values:
        lines.append("  Top valores:")
        for val, cnt in col.top_values:
            lines.append(f"    {val:<20} → {cnt}")
    return "\n".join(lines)


def write_txt_report(summary: DataSummary, output_path: str) -> None:
    """Genera un reporte en texto plano."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sep = _txt_separator()

    lines = [
        sep,
        "  REPORTE AUTOMÁTICO DE DATOS",
        f"  Generado: {now}",
        sep,
        f"  Filas totales       : {summary.total_rows}",
        f"  Columnas totales    : {summary.total_columns}",
        f"  Filas duplicadas    : {summary.duplicate_rows} ({summary.duplicate_pct}%)",
        f"  Columnas numéricas  : {len(summary.numeric_columns)}",
        f"  Columnas categóricas: {len(summary.categorical_columns)}",
        f"  Columnas datetime   : {len(summary.datetime_columns)}",
        sep,
        "  DETALLE POR COLUMNA",
        sep,
    ]

    for col in summary.columns:
        lines.append(_txt_column_block(col))
        lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ──────────────────────────────────────────────
# Reporte HTML
# ──────────────────────────────────────────────

def _html_column_card(col: ColumnSummary) -> str:
    """Genera la tarjeta HTML para una columna."""
    stats_html = ""
    if col.stats:
        rows = "".join(
            f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in col.stats.items()
        )
        stats_html = f"<table class='stats-table'><tbody>{rows}</tbody></table>"

    top_html = ""
    if col.top_values:
        max_count = col.top_values[0][1] if col.top_values else 1
        bars = ""
        for val, cnt in col.top_values:
            pct = round(cnt / max_count * 100)
            bars += (
                f"<div class='bar-row'>"
                f"<span class='bar-label'>{val}</span>"
                f"<div class='bar-track'><div class='bar-fill' style='width:{pct}%'></div></div>"
                f"<span class='bar-count'>{cnt}</span>"
                f"</div>"
            )
        top_html = f"<div class='bar-chart'>{bars}</div>"

    null_color = "red" if col.null_pct > 20 else ("orange" if col.null_pct > 5 else "green")

    return f"""
    <div class='col-card'>
      <div class='col-header'>
        <span class='col-name'>{col.name}</span>
        <span class='col-dtype'>{col.dtype}</span>
      </div>
      <div class='col-meta'>
        <span>Nulos: <strong style='color:{null_color}'>{col.null_count} ({col.null_pct}%)</strong></span>
        <span>Únicos: <strong>{col.unique_count}</strong></span>
      </div>
      {stats_html}
      {top_html}
    </div>"""


def write_html_report(summary: DataSummary, output_path: str) -> None:
    """Genera un reporte visual en HTML."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cards = "\n".join(_html_column_card(col) for col in summary.columns)

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Reporte Automático</title>
<style>
  :root {{
    --bg: #0f1117; --surface: #1a1d27; --border: #2e3145;
    --accent: #6c63ff; --text: #e2e8f0; --muted: #8892a4;
    --green: #4ade80; --orange: #fb923c; --red: #f87171;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); padding: 2rem; }}
  h1 {{ font-size: 1.8rem; margin-bottom: 0.3rem; }}
  .subtitle {{ color: var(--muted); font-size: 0.9rem; margin-bottom: 2rem; }}
  .overview {{ display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 2.5rem; }}
  .stat-box {{ background: var(--surface); border: 1px solid var(--border); border-radius: 10px;
               padding: 1.2rem 1.8rem; flex: 1; min-width: 140px; }}
  .stat-box .label {{ font-size: 0.75rem; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }}
  .stat-box .value {{ font-size: 2rem; font-weight: 700; color: var(--accent); }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.2rem; }}
  .col-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 1.2rem; }}
  .col-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; }}
  .col-name {{ font-weight: 700; font-size: 1rem; }}
  .col-dtype {{ font-size: 0.7rem; background: #2e3145; padding: 2px 8px; border-radius: 99px; color: var(--muted); }}
  .col-meta {{ display: flex; gap: 1rem; font-size: 0.82rem; color: var(--muted); margin-bottom: 0.8rem; }}
  .stats-table {{ width: 100%; border-collapse: collapse; font-size: 0.82rem; margin-bottom: 0.8rem; }}
  .stats-table td {{ padding: 3px 6px; }}
  .stats-table tr:nth-child(even) td {{ background: rgba(255,255,255,0.03); }}
  .bar-chart {{ display: flex; flex-direction: column; gap: 6px; }}
  .bar-row {{ display: flex; align-items: center; gap: 6px; font-size: 0.75rem; }}
  .bar-label {{ width: 100px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color: var(--muted); }}
  .bar-track {{ flex: 1; height: 8px; background: var(--border); border-radius: 99px; overflow: hidden; }}
  .bar-fill {{ height: 100%; background: var(--accent); border-radius: 99px; }}
  .bar-count {{ width: 35px; text-align: right; color: var(--muted); }}
  footer {{ margin-top: 3rem; text-align: center; font-size: 0.8rem; color: var(--muted); }}
</style>
</head>
<body>
<h1>📊 Reporte Automático de Datos</h1>
<p class="subtitle">Generado el {now} · Script de Automatización v1.0</p>

<div class="overview">
  <div class="stat-box"><div class="label">Filas</div><div class="value">{summary.total_rows:,}</div></div>
  <div class="stat-box"><div class="label">Columnas</div><div class="value">{summary.total_columns}</div></div>
  <div class="stat-box"><div class="label">Duplicados</div><div class="value">{summary.duplicate_rows}</div></div>
  <div class="stat-box"><div class="label">Numéricas</div><div class="value">{len(summary.numeric_columns)}</div></div>
  <div class="stat-box"><div class="label">Categóricas</div><div class="value">{len(summary.categorical_columns)}</div></div>
</div>

<div class="grid">
{cards}
</div>

<footer>Generado automáticamente · report-automation</footer>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
