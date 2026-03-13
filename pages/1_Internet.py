import streamlit as st
import plotly.express as px

from components.kpi_cards import show_kpis

from services.data_manager import DataManager

categoria = st.sidebar.selectbox(
    "Categoría",
    [
        "Overview",
        "Tecnología",
        "Velocidad",
        "Velocidad media",
        "Rangos de velocidad",
        "Banda ancha vs Dial-up",
        "Penetración",
        "Ingresos"
    ]
)


if categoria == "Tecnología":
    
    df = DataManager.load_csv("internet_accesos_tecnologias.csv")

    st.title("🌐 Internet fijo")
    st.header("Accesos por tecnología")

    # filtros

    anios = sorted(df["anio"].unique())

    anio = st.sidebar.selectbox(
        "Seleccionar año",
        anios
    )

    trimestres = sorted(df["trimestre"].unique())

    trimestres = st.sidebar.selectbox(
        "Seleccionar trimestre",
        trimestres
    )

    df_filtered = df[(df["anio"] == anio) & (df["trimestre"] == trimestres)]

    # KPIs

    total = df_filtered["total"].sum()
    fibra = df_filtered["fibra_optica"].sum()
    adsl = df_filtered["adsl"].sum()

    show_kpis(total, fibra, adsl)

    st.divider()

    # gráfico

    st.subheader("Evolución por tecnología")

    df["periodo"] = df["anio"].astype(str) + "-T" + df["trimestre"].astype(str)

    df_long = df.melt(
        id_vars="periodo",
        value_vars=["adsl","cablemodem","fibra_optica","wireless", "otros", "total"],
        var_name="Tecnologia",
        value_name="Accesos"
    )

    fig = px.line(
        df_long,
        x="periodo",
        y="Accesos",
        color="Tecnologia",
        markers=True,
        title="Accesos a Internet por Tecnología"
    )

    st.plotly_chart(fig, use_container_width=True)

elif categoria == "Velocidad":

    st.header("Accesos por velocidad")

elif categoria == "Velocidad media":

    st.title("🌐 Internet fijo")
    st.header("Accesos por velocidad media")

    df = DataManager.load_csv("internet_velocidad_media_descarga.csv")



    # filtros

    anios = sorted(df["anio"].unique())

    anio = st.sidebar.selectbox(
        "Seleccionar año",
        anios
    )

    trimestres = sorted(df["trimestre"].unique())

    trimestres = st.sidebar.selectbox(
        "Seleccionar trimestre",
        trimestres
    )

    df_filtered = df[(df["anio"] == anio) & (df["trimestre"] == trimestres)]

    # KPIs

    # total = df_filtered["total"].sum()
    # fibra = df_filtered["fibra_optica"].sum()
    # adsl = df_filtered["adsl"].sum()

    # show_kpis(total, fibra, adsl)

    # st.divider()

    # gráfico

    st.subheader("Evolución por tecnología")

    df["periodo"] = df["anio"].astype(str) + "-T" + df["trimestre"].astype(str)

    df_long = df.melt(
        id_vars="periodo",
        value_vars=["Mbps"],
        var_name="VMD",
        value_name="Accesos"
    )

    fig = px.line(
        df_long,
        x="periodo",
        y="Accesos",
        color="VMD",
        markers=True,
        title="Accesos por velocidad media"
    )

    st.plotly_chart(fig, use_container_width=True)


elif categoria == "Penetración":
    st.header("Penetración de Internet")



tab1, tab2, tab3 = st.tabs([
    "Tecnología",
    "Velocidad",
    "Penetración"
])

with tab1:
    st.subheader("Tecnología")

with tab2:
    st.subheader("Velocidad")

with tab3:
    st.subheader("Penetración")