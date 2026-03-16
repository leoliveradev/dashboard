"""
kpi_cards.py
────────────
Componentes de KPI genéricos y reutilizables.

La función principal `show_kpis` recibe una lista de dicts con
la estructura de cada métrica, sin asumir nombres de columnas.
"""

import streamlit as st


def show_kpis(metrics: list[dict]) -> None:
    """
    Renderiza una fila de KPIs.

    Parameters
    ----------
    metrics : lista de dicts con las siguientes claves:
        - label   (str)         : Etiqueta del KPI.
        - value   (int | float) : Valor principal.
        - delta   (float | None): Variación porcentual vs período anterior.
        - format  (str)         : Formato del valor, ej. "{:,.0f}" o "{:.2f} Mbps".
        - help    (str | None)  : Tooltip de ayuda (opcional).

    Ejemplo
    -------
    show_kpis([
        {"label": "Accesos totales", "value": 12_345_678, "delta": 3.2,  "format": "{:,.0f}"},
        {"label": "Fibra óptica",    "value":  4_200_000, "delta": 12.1, "format": "{:,.0f}"},
        {"label": "Vel. media",      "value":        85.3, "delta": 5.0,  "format": "{:.1f} Mbps"},
    ])
    """
    cols = st.columns(len(metrics))

    for col, m in zip(cols, metrics):
        value_str = m.get("format", "{:,.0f}").format(m["value"])
        delta     = m.get("delta")
        help_text = m.get("help")

        if delta is not None:
            delta_str = f"{delta:+.1f}% vs trimestre anterior"
        else:
            delta_str = None

        col.metric(
            label=m["label"],
            value=value_str,
            delta=delta_str,
            help=help_text,
        )


def show_kpi_row_with_icon(metrics: list[dict]) -> None:
    """
    Variante con ícono y tarjeta personalizada usando st.container.

    Mismo formato que show_kpis pero con un campo extra:
        - icon (str): emoji para mostrar junto al label.
    """
    cols = st.columns(len(metrics))
    for col, m in zip(cols, metrics):
        with col:
            icon      = m.get("icon", "")
            value_str = m.get("format", "{:,.0f}").format(m["value"])
            delta     = m.get("delta")

            delta_str = f"{delta:+.1f}%" if delta is not None else ""
            delta_color = "green" if (delta or 0) >= 0 else "red"

            st.markdown(
                f"""
                <div style="
                    border: 1px solid rgba(0,0,0,0.08);
                    border-radius: 10px;
                    padding: 16px 20px;
                    margin-bottom: 8px;
                ">
                    <div style="font-size:13px; color:#64748b; margin-bottom:4px;">
                        {icon} {m['label']}
                    </div>
                    <div style="font-size:26px; font-weight:600; color:#1e293b;">
                        {value_str}
                    </div>
                    <div style="font-size:12px; color:{delta_color}; margin-top:4px;">
                        {delta_str}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )