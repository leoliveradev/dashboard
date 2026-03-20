"""
charts.py
─────────
Funciones de gráficos reutilizables basadas en Plotly Express.

Cada función aplica el tema base (theme.py) automáticamente.
Las páginas solo eligen qué datos mostrar, no cómo configurar el gráfico.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config.theme import PLOTLY_BASE_LAYOUT, COLOR_SEQUENCE, COLORS


def _apply_theme(fig: go.Figure, y_tickformat: str = ",.0f") -> go.Figure:
    """
    Aplica el layout base y el formato numérico argentino a cualquier figura Plotly.

    Parameters
    ----------
    y_tickformat : formato d3 para el eje Y.
        ",.0f"  → enteros con separador de miles (default)
        ",.1f"  → un decimal
        ",.2f"  → dos decimales
    """
    fig.update_layout(**PLOTLY_BASE_LAYOUT)
    fig.update_layout(
        separators=",.",
        yaxis={"tickformat": y_tickformat, "separatethousands": True},
    )
    return fig


def line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    color: str | None = None,
    title: str = "",
    color_map: dict | None = None,
    labels: dict | None = None,
    markers: bool = True,
    y_tickformat: str = ",.0f",
) -> go.Figure:
    """
    Gráfico de líneas estándar para series temporales.

    Parameters
    ----------
    df           : DataFrame en formato largo.
    x            : Columna del eje X (normalmente "periodo").
    y            : Columna del eje Y (normalmente "Accesos" o similar).
    color        : Columna para separar series por color.
    title        : Título del gráfico.
    color_map    : Dict {valor_color → hex}, ej. COLORS de theme.py.
    labels       : Dict renombre de columnas para los ejes/leyenda.
    markers      : Mostrar marcadores en los puntos de datos.
    y_tickformat : Formato d3 del eje Y. ",.0f" enteros, ",.1f" un decimal, etc.
    """
    fig = px.line(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        markers=markers,
        color_discrete_map=color_map,
        color_discrete_sequence=COLOR_SEQUENCE,
        labels=labels or {},
    )
    fig.update_traces(line={"width": 2})
    return _apply_theme(fig, y_tickformat)


def bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    color: str | None = None,
    title: str = "",
    color_map: dict | None = None,
    labels: dict | None = None,
    barmode: str = "group",
    y_tickformat: str = ",.0f",
) -> go.Figure:
    """Gráfico de barras agrupadas o apiladas."""
    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        barmode=barmode,
        color_discrete_map=color_map,
        color_discrete_sequence=COLOR_SEQUENCE,
        labels=labels or {},
    )
    return _apply_theme(fig, y_tickformat)


def choropleth_argentina(
    df: pd.DataFrame,
    location_col: str,
    value_col: str,
    title: str = "",
    color_scale: str = "Blues",
    y_tickformat: str = ",.0f",
) -> go.Figure:
    """
    Mapa coroplético de Argentina por provincia.

    Requiere que `location_col` contenga los nombres de provincia
    en el mismo formato que el GeoJSON de Argentina.
    """
    fig = px.choropleth(
        df,
        locations=location_col,
        color=value_col,
        title=title,
        color_continuous_scale=color_scale,
        locationmode="country names",
    )
    fig.update_geos(
        fitbounds="locations",
        visible=False,
    )
    return _apply_theme(fig, y_tickformat)


def area_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    color: str | None = None,
    title: str = "",
    color_map: dict | None = None,
    y_tickformat: str = ",.0f",
) -> go.Figure:
    """Gráfico de área apilada, útil para composición en el tiempo."""
    fig = px.area(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        color_discrete_map=color_map,
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    return _apply_theme(fig, y_tickformat)