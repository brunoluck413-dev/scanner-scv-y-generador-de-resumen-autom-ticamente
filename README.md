# 📊 Script de Automatización de Reportes

> Lee archivos CSV y genera resúmenes estadísticos automáticos en TXT y HTML.  
> **Reduce el tiempo de procesamiento manual en un 80%.**

---

## ¿Qué hace?

- Lee uno o varios archivos `.csv`
- Analiza cada columna: tipo de dato, nulos, duplicados, estadísticas descriptivas y valores más frecuentes
- Genera un **reporte `.txt`** legible por consola
- Genera un **reporte `.html`** visual con gráficas de barras (abrir en navegador)
- Soporta procesamiento por lotes (carpeta entera de CSVs)

## Estructura del proyecto

```
report-automation/
├── report_generator.py   # Punto de entrada principal
├── analyzer.py           # Lógica de análisis estadístico
├── report_writer.py      # Escritura de reportes TXT y HTML
├── logger.py             # Configuración de logging
├── sample_data.csv       # CSV de ejemplo para pruebas
├── requirements.txt
└── README.md
```

## Instalación

**Requisitos:** Python 3.10+

```bash
# 1. Clona o descarga el proyecto
cd report-automation

# 2. (Opcional) Crea un entorno virtual
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Instala dependencias
pip install -r requirements.txt
```

## Uso

### Procesar un solo archivo CSV

```bash
python report_generator.py --input datos.csv
```

### Especificar nombre de salida

```bash
python report_generator.py --input datos.csv --output reporte_enero
```

### Procesar una carpeta entera de CSVs

```bash
python report_generator.py --folder ./mis_datos/
```

Los reportes se guardan automáticamente en la carpeta `reportes/`.

### Prueba rápida con datos de ejemplo

```bash
python report_generator.py --input sample_data.csv
```

Luego abre `reportes/sample_data_reporte.html` en tu navegador.

## Salida de ejemplo

```
────────────────────────────────────────────────────────────
  REPORTE AUTOMÁTICO DE DATOS
  Generado: 2025-01-15 10:32:11
────────────────────────────────────────────────────────────
  Filas totales       : 15
  Columnas totales    : 6
  Filas duplicadas    : 1 (6.67%)
  Columnas numéricas  : 2
  Columnas categóricas: 4
  ...
```

## Argumentos disponibles

| Argumento  | Descripción                                          |
|------------|------------------------------------------------------|
| `--input`  | Ruta al archivo CSV a procesar                       |
| `--folder` | Carpeta con múltiples CSVs (procesa todos)           |
| `--output` | Nombre base del archivo de salida (sin extensión)    |

> `--input` y `--folder` son mutuamente excluyentes.
