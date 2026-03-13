import streamlit as st

st.set_page_config(
    page_title="Indicadores - ENACOM",
    page_icon="📡",
    layout="wide"
)

st.title("📡 Indicadores - ENACOM")

st.markdown("""
Este dashboard explora datos del sector de telecomunicaciones en Argentina.

Fuentes:
- ENACOM
- Series históricas del sector

Servicios analizados:

- 🌐 Internet fijo
- 📱 Telefonía móvil
- ☎️ Telefonía fija
- 📺 TV paga
- 📦 Servicios postales
""")

st.info("Seleccioná una sección en el menú lateral.")