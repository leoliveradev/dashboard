import streamlit as st

from services.data_manager import DataManager

df = DataManager.load_csv("comunicaciones_moviles_accesos.csv")

st.title("📱 Telefonía móvil")

st.subheader("Accesos móviles")

st.dataframe(df)