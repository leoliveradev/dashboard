import streamlit as st


def show_kpis(total, fibra_optica, adsl):

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Accesos totales",
        f"{total:,.0f}"
    )

    col2.metric(
        "Fibra óptica",
        f"{fibra_optica:,.0f}"
    )

    col3.metric(
        "ADSL",
        f"{adsl:,.0f}"
    )