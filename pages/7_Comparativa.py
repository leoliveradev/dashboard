"""
6_Comparativa.py
────────────────
Vista transversal: compara ingresos y accesos entre todos los servicios.
Esta página es la única que carga múltiples grupos de CSVs a la vez.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from config.constants import InternetCSV, MovilCSV, TVCSVs, TelefoniaCSV
from config.theme import PLOTLY_BASE_LAYOUT, COLORS
from components.page_setup import setup_page
from services.data_manager import DataManager, DataLoadError
from services.transformers import add_periodo_col, sort_by_periodo, last_period_delta
from components.sidebar import render_sidebar
from components.kpi_cards import show_kpis
from components.charts import bar_chart, line_chart


st.set_page_config(page_title="Comparativa · ENACOM", page_icon="📊", layout="wide")

setup_page()

CATEGORIES = ["Ingresos por servicio", "Accesos por servicio"]

categoria = render_sidebar(CATEGORIES, key="comp_categoria")
st.title("📊 Comparativa entre servicios")


def try_load(filename: str) -> pd.DataFrame | None:
    """Carga silenciosa: devuelve None si el archivo no existe."""
    try:
        return DataManager.load(filename)
    except DataLoadError:
        return None


def detect_col(df: pd.DataFrame, *keywords) -> str | None:
    """Detecta la primera columna que contenga alguna de las keywords."""
    for kw in keywords:
        col = next((c for c in df.columns if kw in c), None)
        if col:
            return col
    return None


# ── Ingresos por servicio ─────────────────────────────────────────────────────

if categoria == "Ingresos por servicio":
    st.header("Ingresos comparados por servicio")
    st.caption("Ingresos declarados en miles de pesos. Comparación histórica entre sectores.")

    SOURCES = {
        "Internet fijo": (InternetCSV.INGRESOS,    "internet"),
        "Móvil":         (MovilCSV.INGRESOS,        "movil"),
        "TV paga":       (TVCSVs.INGRESOS,           "tv"),
        "Tel. fija":     (TelefoniaCSV.FIJA_INGRESOS,"telefonia"),
    }

    series = []
    kpis   = []

    for servicio, (filename, _) in SOURCES.items():
        df = try_load(filename)
        if df is None:
            continue

        ing_col = detect_col(df, "ingreso", "miles", "monto")
        if ing_col is None:
            continue

        df = sort_by_periodo(add_periodo_col(df))
        val, delta = last_period_delta(df, ing_col)

        kpis.append({
            "label":  servicio,
            "value":  val,
            "delta":  delta,
            "format": "{:,.0f}",
        })

        df_s = df[["periodo", ing_col]].copy()
        df_s["Servicio"] = servicio
        df_s = df_s.rename(columns={ing_col: "Ingresos"})
        series.append(df_s)

    if not series:
        st.warning("No se encontraron archivos de ingresos.", icon="⚠️")
        st.stop()

    show_kpis(kpis)
    st.divider()

    df_all = pd.concat(series, ignore_index=True)

    tab1, tab2 = st.tabs(["Líneas", "Barras agrupadas"])

    with tab1:
        fig = line_chart(df_all, "periodo", "Ingresos", "Servicio",
                         title="Ingresos por servicio — evolución histórica", markers=False)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        fig = bar_chart(df_all, "periodo", "Ingresos", "Servicio",
                        title="Ingresos por trimestre y servicio", barmode="group")
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("Ver tabla de datos"):
        st.dataframe(df_all, use_container_width=True)


# ── Accesos por servicio ──────────────────────────────────────────────────────

elif categoria == "Accesos por servicio":
    st.header("Accesos comparados por servicio")
    st.caption("Cantidad de accesos / líneas activas. Escala distinta entre servicios.")

    SOURCES = {
        "Internet fijo": (InternetCSV.TECNOLOGIAS, "total", "acceso"),
        "Móvil":         (MovilCSV.ACCESOS,         "total", "linea", "acceso"),
        "TV paga":       (TVCSVs.ACCESOS,            "total", "acceso"),
        "Tel. fija":     (TelefoniaCSV.FIJA_ACCESOS, "total", "acceso", "linea"),
    }

    series = []
    kpis   = []

    for servicio, (filename, *keywords) in SOURCES.items():
        df = try_load(filename)
        if df is None:
            continue

        acc_col = detect_col(df, *keywords)
        if acc_col is None:
            continue

        df = sort_by_periodo(add_periodo_col(df))
        val, delta = last_period_delta(df, acc_col)

        kpis.append({
            "label":  servicio,
            "value":  val,
            "delta":  delta,
            "format": "{:,.0f}",
        })

        df_s = df[["periodo", acc_col]].copy()
        df_s["Servicio"] = servicio
        df_s = df_s.rename(columns={acc_col: "Accesos"})
        series.append(df_s)

    if not series:
        st.warning("No se encontraron archivos de accesos.", icon="⚠️")
        st.stop()

    show_kpis(kpis)
    st.divider()

    df_all = pd.concat(series, ignore_index=True)

    st.info(
        "Las escalas difieren significativamente entre servicios. "
        "Usá los filtros de la leyenda del gráfico para comparar pares.",
        icon="ℹ️",
    )

    fig = line_chart(df_all, "periodo", "Accesos", "Servicio",
                     title="Accesos por servicio — evolución histórica", markers=False)
    st.plotly_chart(fig, use_container_width=True)