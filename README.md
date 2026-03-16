# Indicadores ENACOM — Dashboard

Dashboard de indicadores del sector de telecomunicaciones de Argentina,
basado en datos abiertos de ENACOM.

## Estructura del proyecto

```
dashboard/
├── app.py                        # Entry point
├── requirements.txt
├── config/
│   ├── settings.py               # Rutas, encoding, metadata de la app
│   ├── constants.py              # Nombres de archivos CSV y columnas
│   └── theme.py                  # Colores y layout de Plotly
├── services/
│   ├── data_manager.py           # Carga y cache de CSVs
│   ├── data_validator.py         # Validación de columnas y datos
│   └── transformers.py           # Transformaciones de pandas (funciones puras)
├── components/
│   ├── kpi_cards.py              # Métricas genéricas
│   ├── charts.py                 # Gráficos reutilizables (Plotly)
│   ├── filters.py                # Widgets de filtro para el sidebar
│   └── sidebar.py                # Sidebar común
├── pages/
│   ├── 1_Internet.py
│   ├── 2_Movil.py
│   ├── 3_TV.py
│   ├── 4_Telefonia.py
│   ├── 5_Postal.py
│   └── 6_Comparativa.py
└── data/                         # CSVs de ENACOM (no incluidos en el repo)
```

## Instalación y ejecución

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Principios de arquitectura

**Dependencia descendente**: las capas solo conocen a la que está debajo.
`pages → components → services → config`. Nunca al revés.

**Una sola fuente de verdad por responsabilidad**:
- Nombres de archivos → `config/constants.py`
- Carga y cache → `services/data_manager.py`
- Lógica de pandas → `services/transformers.py`
- Colores y estilo → `config/theme.py`

**Páginas livianas**: cada página solo orquesta.
El patrón es siempre: `load → validate → transform → render`.

## Agregar una nueva página

1. Agregar el nombre del CSV en `config/constants.py`.
2. Crear `pages/N_NombreServicio.py` copiando la estructura de cualquier página existente.
3. Importar las funciones necesarias de `services/` y `components/`.
4. La página no debe contener lógica de pandas ni strings de archivos CSV directamente.

## Agregar un nuevo gráfico reutilizable

Agregar una función en `components/charts.py` siguiendo el patrón existente:
recibe un DataFrame y parámetros, aplica `_apply_theme()`, devuelve una figura Plotly.