"""
kpi_cards.py
────────────
Componentes de KPI genéricos y reutilizables.
Usa formato numérico argentino: punto como separador de miles, coma para decimales.
"""

import streamlit as st


def fmt_ar(format_str: str, value: float) -> str:
    """
    Formatea un número en formato argentino:
      - Separador de miles: punto  (.)
      - Separador decimal:  coma   (,)

    Acepta los mismos format_str que se usan en toda la app:
      "{:,.0f}"        → "1.234.567"
      "{:.2f}"         → "12,34"
      "{:.1f} Mbps"    → "85,3 Mbps"
      "{:+.1f}%"       → "+3,2%"
      "{:.1f}%"        → "42,5%"

    El truco: Python formatea primero con coma/punto anglosajón,
    luego hacemos el swap con un carácter temporal (#).
    """
    formatted = format_str.format(value)
    # swap: , → # (temporal), . → , (decimales), # → . (miles)
    return formatted.replace(",", "#").replace(".", ",").replace("#", ".")


def show_kpis(metrics: list[dict]) -> None:
    """
    Renderiza una fila de KPIs con formato numérico argentino.

    Parameters
    ----------
    metrics : lista de dicts:
        - label   (str)         : Etiqueta del KPI.
        - value   (int | float) : Valor principal.
        - delta   (float | None): Variación porcentual vs período anterior.
        - format  (str)         : Formato del valor, ej. "{:,.0f}" o "{:.2f} Mbps".
        - help    (str | None)  : Tooltip de ayuda (opcional).

    Ejemplo
    -------
    show_kpis([
        {"label": "Accesos totales", "value": 12_345_678, "delta": 3.2,  "format": "{:,.0f}"},
        {"label": "Vel. media",      "value": 85.3,       "delta": 5.0,  "format": "{:.1f} Mbps"},
    ])
    """
    cols = st.columns(len(metrics))

    for col, m in zip(cols, metrics):
        value_str = fmt_ar(m.get("format", "{:,.0f}"), m["value"])
        delta     = m.get("delta")
        help_text = m.get("help")

        if delta is not None:
            delta_str = fmt_ar("{:+.1f}%", delta) + " vs trim. anterior"
        else:
            delta_str = None

        col.metric(
            label=m["label"],
            value=value_str,
            delta=delta_str,
            help=help_text,
        )


def show_kpi_row_with_icon(metrics: list[dict]) -> None:
    """Variante con ícono y tarjeta personalizada."""
    cols = st.columns(len(metrics))
    for col, m in zip(cols, metrics):
        with col:
            icon      = m.get("icon", "")
            value_str = fmt_ar(m.get("format", "{:,.0f}"), m["value"])
            delta     = m.get("delta")

            delta_str   = fmt_ar("{:+.1f}%", delta) if delta is not None else ""
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