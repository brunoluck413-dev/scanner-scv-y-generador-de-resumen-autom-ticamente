"""
analyzer.py
-----------
Módulo de análisis estadístico de DataFrames.
Extrae métricas clave: tipos de datos, estadísticas descriptivas,
valores nulos, duplicados y distribución de columnas categóricas.
"""

from dataclasses import dataclass, field
from typing import Any

import pandas as pd


@dataclass
class ColumnSummary:
    """Resumen estadístico de una columna individual."""
    name: str
    dtype: str
    null_count: int
    null_pct: float
    unique_count: int
    stats: dict[str, Any] = field(default_factory=dict)
    top_values: list[tuple[str, int]] = field(default_factory=list)


@dataclass
class DataSummary:
    """Resumen completo de un DataFrame."""
    total_rows: int
    total_columns: int
    duplicate_rows: int
    duplicate_pct: float
    columns: list[ColumnSummary]
    numeric_columns: list[str]
    categorical_columns: list[str]
    datetime_columns: list[str]


def _summarize_numeric(series: pd.Series) -> dict[str, Any]:
    """Calcula estadísticas descriptivas para columnas numéricas."""
    desc = series.describe()
    return {
        "min": round(desc["min"], 4),
        "max": round(desc["max"], 4),
        "mean": round(desc["mean"], 4),
        "median": round(series.median(), 4),
        "std": round(desc["std"], 4),
        "q25": round(desc["25%"], 4),
        "q75": round(desc["75%"], 4),
    }


def _summarize_categorical(series: pd.Series, top_n: int = 5) -> list[tuple[str, int]]:
    """Retorna los N valores más frecuentes de una columna categórica."""
    return [(str(val), int(cnt)) for val, cnt in series.value_counts().head(top_n).items()]


def analyze_dataframe(df: pd.DataFrame) -> DataSummary:
    """
    Analiza un DataFrame completo y retorna un DataSummary con toda
    la información estadística relevante.

    Args:
        df: DataFrame de pandas a analizar.

    Returns:
        DataSummary con métricas por columna y globales.
    """
    total_rows = len(df)
    duplicate_rows = int(df.duplicated().sum())
    duplicate_pct = round((duplicate_rows / total_rows * 100) if total_rows > 0 else 0, 2)

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    datetime_cols = df.select_dtypes(include=["datetime"]).columns.tolist()

    column_summaries = []
    for col in df.columns:
        series = df[col]
        null_count = int(series.isna().sum())
        null_pct = round((null_count / total_rows * 100) if total_rows > 0 else 0, 2)
        unique_count = int(series.nunique())

        stats: dict[str, Any] = {}
        top_values: list[tuple[str, int]] = []

        if col in numeric_cols:
            stats = _summarize_numeric(series.dropna())
        elif col in categorical_cols:
            top_values = _summarize_categorical(series)

        column_summaries.append(
            ColumnSummary(
                name=col,
                dtype=str(series.dtype),
                null_count=null_count,
                null_pct=null_pct,
                unique_count=unique_count,
                stats=stats,
                top_values=top_values,
            )
        )

    return DataSummary(
        total_rows=total_rows,
        total_columns=len(df.columns),
        duplicate_rows=duplicate_rows,
        duplicate_pct=duplicate_pct,
        columns=column_summaries,
        numeric_columns=numeric_cols,
        categorical_columns=categorical_cols,
        datetime_columns=datetime_cols,
    )
