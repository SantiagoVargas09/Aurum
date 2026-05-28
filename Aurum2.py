# ============================================
# IMPORTACIONES
# ============================================
import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import os

st.set_page_config(
    page_title="Aurum · Vino de Maracuyá",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.stApp { background-color: #fdf6e3; }
.stApp, .stMarkdown, p, label { color: #2c1a0e; }

.titulo-principal {
    font-size: 2.8rem; font-weight: bold; color: #3e2005;
    text-align: center; letter-spacing: 8px;
    text-transform: uppercase; font-family: Georgia, serif; margin-bottom: 0;
}
.subtitulo {
    text-align: center; color: #7a4f1d; font-size: 1rem;
    margin-bottom: 4px; font-style: italic;
    font-family: Georgia, serif; letter-spacing: 2px;
}
/* subtítulo descriptivo debajo de cada gráfica */
.grafica-subtitulo {
    color: #3e2005 !important; font-family: Georgia, serif;
    font-size: 0.92rem; font-weight: 600; margin-bottom: 6px;
}

thead tr th {
    background-color: #1c1008 !important; color: #e8b84b !important;
    font-family: Georgia, serif !important; letter-spacing: 1px !important;
}
tbody tr:nth-child(even) { background-color: #fdf0d0 !important; }
tbody tr:nth-child(odd)  { background-color: #fffdf5 !important; }
tbody tr td { color: #2c1a0e !important; }

div[data-testid="metric-container"] {
    background-color: #fffdf5; border: 1.5px solid #c8922a;
    border-radius: 12px; padding: 12px;
    box-shadow: 0 2px 8px rgba(62,32,5,0.10);
}
div[data-testid="metric-container"] > div > div:first-child {
    color: #3e2005 !important; font-weight: 700; font-family: Georgia, serif;
}
div[data-testid="metric-container"] label { color: #7a4f1d !important; font-weight: 600; }

hr { border-color: #d4a96a; opacity: 0.5; }

.stButton > button {
    background-color: #c8922a; color: #fffdf5; border-radius: 8px;
    border: none; font-weight: 600; letter-spacing: 1px;
}
.stButton > button:hover { background-color: #3e2005; color: #e8b84b; }

.stTextArea textarea, .stTextInput input {
    border: 1.5px solid #c8922a; border-radius: 8px;
    background-color: #fffdf5; color: #2c1a0e;
}

div[data-testid="stInfo"]    { background-color: #fdf0d0; border-left: 4px solid #c8922a; color: #2c1a0e; }
div[data-testid="stSuccess"] { background-color: #f0ead0; border-left: 4px solid #7a4f1d; color: #2c1a0e; }

button[data-baseweb="tab"] {
    color: #7a4f1d !important; font-weight: 600 !important;
    font-family: Georgia, serif !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #3e2005 !important; border-bottom: 2px solid #c8922a !important;
}

h2, h3 { color: #3e2005 !important; font-family: Georgia, serif !important; }
.stCaption { color: #7a4f1d !important; font-style: italic !important; }
</style>
""", unsafe_allow_html=True)


def cargar_imagen_local(ruta):
    if not os.path.exists(ruta):
        return None, None
    ext  = os.path.splitext(ruta)[1].lower()
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}.get(ext, "image/png")
    with open(ruta, "rb") as f:
        return base64.b64encode(f.read()).decode(), mime


# ══════════════════════════════════════════════════════
#   RUTAS DE ARCHIVOS 
# ══════════════════════════════════════════════════════
RUTA_LOGO  = r"LOGO + QR/Aurum.jpeg"
RUTA_QR    = r"LOGO + QR/qr-code.png"
RUTA_EXCEL = r"xlsx/BALANCE.xlsx"
# ══════════════════════════════════════════════════════

img_b64, tipo    = cargar_imagen_local(RUTA_LOGO)
qr_b64,  qr_tipo = cargar_imagen_local(RUTA_QR)


@st.cache_data
def cargar_balance(ruta):
    if not os.path.exists(ruta):
        return None
    return pd.read_excel(ruta, sheet_name=0, header=None)

raw = cargar_balance(RUTA_EXCEL)

ingredientes = {
    "Componente": [
        "Pulpa de maracuyá (P)", "Miel (M)", "Azúcar (Az)", "Agua (A)",
        "CO₂ — gas de purga", "Sólidos insolubles (S)",
        "Etanol en vino (C₂H₅OH)", "Agua en vino (H₂O)", "Vino final (V)"
    ],
    "Flujo (kg/h)": [
        116500.0, 56000.0, 6500.0, 150000.0,
        31303.10, 11650.0, 32766.90, 253280.0, 286046.90
    ],
    "Tipo": [
        "Entrada","Entrada","Entrada","Entrada",
        "Salida","Salida","Composición vino","Composición vino","Salida"
    ],
    "Fracción másica": [
        "35.41%","17.02%","1.98%","45.59%",
        "9.51%","3.54%","11.45%","88.54%","86.94% del total"
    ]
}
df = pd.DataFrame(ingredientes)

rendimientos = {
    "Etapa":          ["Mezclado", "Fermentación", "Filtrado", "Global"],
    "Pérdida (kg/h)": [0.0, 31303.10, 11650.0, 42953.10],
    "% Pérdida":      [0.0, 9.51, 3.54, 13.06],
    "% Rendimiento":  [100.0, 90.49, 96.09, 86.94]
}
df_rend = pd.DataFrame(rendimientos)

df_vino = pd.DataFrame({
    "Componente": ["Etanol (C₂H₅OH)", "Agua (H₂O)", "Sólidos"],
    "kg/h":       [32766.90, 253280.0, 0.0],
    "Fracción %": [11.45, 88.54, 0.0]
})

PALETA = ["#c8922a", "#e8b84b", "#7a4f1d", "#3e2005",
          "#d4a96a", "#f0d080", "#a0622a", "#1c1008"]


def hacer_layout(titulo, label_x="", label_y="", angulo_x=0, mostrar_leyenda=False):
    fuente_ejes   = dict(color="#2c1a0e", size=13, family="Georgia")
    fuente_ticks  = dict(color="#2c1a0e", size=11, family="Georgia")
    fuente_titulo = dict(color="#1c1008", size=16, family="Georgia")
    return dict(
        plot_bgcolor  = "#fdf6e3",
        paper_bgcolor = "#fdf6e3",
        font  = dict(color="#2c1a0e", family="Georgia"),
        title = dict(
            text = titulo,
            font = fuente_titulo,
            x    = 0.01
        ),
        showlegend = mostrar_leyenda,
        legend     = dict(font=dict(color="#2c1a0e", family="Georgia")),
        xaxis = dict(
            title      = label_x,
            title_font = fuente_ejes,
            tickfont   = fuente_ticks,
            tickangle  = angulo_x,
            linecolor  = "#c8922a",
            gridcolor  = "#e8d5b0"
        ),
        yaxis = dict(
            title      = label_y,
            title_font = fuente_ejes,
            tickfont   = fuente_ticks,
            linecolor  = "#c8922a",
            gridcolor  = "#e8d5b0"
        ),
        margin = dict(t=60, b=50, l=60, r=20)
    )


# ─────────────────────────────────────────────
# TÍTULO DEL DASHBOARD
# ─────────────────────────────────────────────
st.markdown('<p class="titulo-principal"> AURUM</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitulo">Dashboard De Balance De Materia Y Energia · Vino De Maracuyá Con Miel</p>',
    unsafe_allow_html=True
)
st.markdown("---")

col_izq, col_der = st.columns([1, 2])


# ══════════════════════════════════════════════
# COLUMNA IZQUIERDA — logo, QR y info del vino
# ══════════════════════════════════════════════
with col_izq:

    c_logo, c_qr = st.columns(2)

    # ── LOGO ──────────────────────────────────────────────────────────────
    
    with c_logo:
        if img_b64 is not None:
            st.markdown(f"""
                <div style="background:#ffffff; border:1.5px solid #d4a96a;
                     border-radius:12px; overflow:hidden;
                     display:flex; flex-direction:column;
                     align-items:center; justify-content:flex-start;
                     padding:8px 6px; box-sizing:border-box; min-height:190px;">
                    <img src="data:{tipo};base64,{img_b64}"
                         style="width:100%; height:130px;
                                object-fit:contain; display:block;
                                flex-shrink:0; background:#ffffff;">
                    <p style="color:#3e2005; font-family:Georgia,serif; font-weight:bold;
                              font-size:0.8rem; margin:6px 0 2px; letter-spacing:2px;
                              text-align:center;">AURUM</p>
                    <p style="color:#7a4f1d; font-style:italic; font-size:0.65rem;
                              margin:0 0 4px; text-align:center;">Vino de Maracuyá</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="background:#ffffff; border:2px dashed #d4a96a;
                     border-radius:12px; min-height:190px; display:flex;
                     flex-direction:column; align-items:center; justify-content:center;">
                    <div style="font-size:52px;"></div>
                    <p style="color:#7a4f1d; font-size:0.68rem; font-style:italic;
                              margin:4px 0 0; text-align:center;">Sin logo</p>
                    <p style="color:#c8922a; font-size:0.62rem; margin:2px 0 0;">Edita RUTA_LOGO</p>
                </div>
            """, unsafe_allow_html=True)

    # ── QR ────────────────────────────────────────────────────────────────
    with c_qr:
        if qr_b64 is not None:
            st.markdown(f"""
                <div style="background:#ffffff; border:1.5px solid #d4a96a;
                     border-radius:12px; overflow:hidden;
                     display:flex; flex-direction:column;
                     align-items:center; justify-content:flex-start;
                     padding:8px 6px; box-sizing:border-box; min-height:190px;">
                    <img src="data:{qr_tipo};base64,{qr_b64}"
                         style="width:100%; height:130px;
                                object-fit:contain; display:block;
                                flex-shrink:0; background:#ffffff;">
                    <p style="color:#7a4f1d; font-size:0.65rem; font-style:italic;
                              margin:6px 0 4px; text-align:center;">Escanea para más info</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="background:#fdf0d0; border:2px dashed #c8922a;
                     border-radius:12px; min-height:190px; display:flex;
                     flex-direction:column; align-items:center; justify-content:center;">
                    <div style="font-size:40px; opacity:0.4;"></div>
                    <p style="color:#c8922a; font-size:0.68rem; font-style:italic;
                              margin:6px 0 0; font-family:Georgia,serif; text-align:center;">
                              Espacio QR<br>reservado</p>
                    <p style="color:#c8922a; font-size:0.62rem; margin:2px 0 0;">Edita RUTA_QR</p>
                </div>
            """, unsafe_allow_html=True)

    # ficha del proceso
    st.markdown("""
        <div style="background:#fffdf5; border:1.5px solid #d4a96a;
             border-radius:12px; padding:12px 14px; margin-top:12px;
             font-size:0.85rem; color:#2c1a0e;">
            <table style="width:100%; border-collapse:collapse;">
                <tr>
                    <td style="padding:4px 6px;"><b>Tipo</b></td>
                    <td style="padding:4px 6px; color:#7a4f1d;">Vino artesanal frutal</td>
                </tr>
                <tr style="background:#fdf0d0;">
                    <td style="padding:4px 6px;"><b>Base</b></td>
                    <td style="padding:4px 6px; color:#7a4f1d;">Maracuyá + Miel</td>
                </tr>
                <tr>
                    <td style="padding:4px 6px;"><b>Entrada total</b></td>
                    <td style="padding:4px 6px; color:#7a4f1d;">329,000 kg/h</td>
                </tr>
                <tr style="background:#fdf0d0;">
                    <td style="padding:4px 6px;"><b>Vino producido</b></td>
                    <td style="padding:4px 6px; color:#7a4f1d;">286,047 kg/h</td>
                </tr>
                <tr>
                    <td style="padding:4px 6px;"><b>Etanol en vino</b></td>
                    <td style="padding:4px 6px; color:#7a4f1d;">11.45% másico</td>
                </tr>
                <tr style="background:#fdf0d0;">
                    <td style="padding:4px 6px;"><b>Reacción</b></td>
                    <td style="padding:4px 6px; color:#7a4f1d;">C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂</td>
                </tr>
                <tr>
                    <td style="padding:4px 6px;"><b>Rendimiento global</b></td>
                    <td style="padding:4px 6px; color:#7a4f1d;">86.94%</td>
                </tr>
            </table>
        </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# COLUMNA DERECHA — tabla de balance + métricas
# ══════════════════════════════════════════════
with col_der:

    st.subheader(" Balance Global de Masa")
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("###  Valores Clave del Balance")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Entrada total",    "329,000 kg/h")
    m2.metric("Vino producido",   "286,047 kg/h")
    m3.metric("Etanol en vino",   "11.45%")
    m4.metric("Rendimiento",      "86.94%")

    m5, m6, m7, m8 = st.columns(4)
    m5.metric("CO₂ generado",      "31,303 kg/h")
    m6.metric("Sólidos filtrados",  "11,650 kg/h")
    m7.metric("Qr fermentación",    "37,288,740 kJ/h")
    m8.metric("Q chaqueta",         "25,463,642 kJ/h")


# ─────────────────────────────────────────────
# GRÁFICAS EN TABS
# ─────────────────────────────────────────────
st.markdown("---")
st.subheader(" Visualización del Balance")

tab1, tab2, tab3, tab4 = st.tabs([
    " Flujos de entrada",
    " Composición del vino",
    " Rendimientos por etapa",
    " Entradas vs Salidas"
])

# ── Tab 1 ────────────────────────────────────
with tab1:
    st.markdown(
        "<p class='grafica-subtitulo'>Flujo másico de cada componente en la alimentación (kg/h)</p>",
        unsafe_allow_html=True
    )
    df_ent = df[df["Tipo"] == "Entrada"].copy()
    fig1 = px.bar(
        df_ent, x="Componente", y="Flujo (kg/h)",
        color="Componente", text="Flujo (kg/h)",
        color_discrete_sequence=PALETA
    )
    fig1.update_layout(**hacer_layout(
        "Flujos másicos de entrada al proceso (kg/h)",
        label_x="Componente", label_y="Flujo (kg/h)", angulo_x=-20
    ))
    fig1.update_traces(
        textposition="outside", texttemplate="%{y:,.0f}",
        textfont=dict(color="#1c1008", size=11, family="Georgia")
    )
    st.plotly_chart(fig1, use_container_width=True)

# ── Tab 2 ────────────────────────────────────
with tab2:
    st.markdown(
        "<p class='grafica-subtitulo'>Fracción másica de cada componente en el vino producido</p>",
        unsafe_allow_html=True
    )
    df_comp = df_vino[df_vino["Fracción %"] > 0].copy()
    fig2 = px.pie(
        df_comp, names="Componente", values="Fracción %",
        color_discrete_sequence=PALETA
    )
    fig2.update_layout(
        plot_bgcolor  = "#fdf6e3",
        paper_bgcolor = "#fdf6e3",
        font   = dict(color="#2c1a0e", family="Georgia"),
        title  = dict(
            text = "Composición del vino final (% másico)",
            font = dict(color="#1c1008", size=16, family="Georgia"),
            x    = 0.01
        ),
        legend = dict(font=dict(color="#2c1a0e", size=12, family="Georgia")),
        margin = dict(t=60, b=20, l=20, r=20)
    )
    fig2.update_traces(
        textposition="inside", textinfo="percent+label",
        textfont=dict(color="#1c1008", size=12, family="Georgia")
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── Tab 3 ────────────────────────────────────
with tab3:
    st.markdown(
        "<p class='grafica-subtitulo'>Porcentaje de rendimiento en cada etapa del proceso productivo</p>",
        unsafe_allow_html=True
    )
    fig3 = px.bar(
        df_rend, x="Etapa", y="% Rendimiento",
        color="Etapa", text="% Rendimiento",
        color_discrete_sequence=PALETA
    )
    fig3.update_layout(**hacer_layout(
        "Rendimiento por etapa del proceso (%)",
        label_x="Etapa", label_y="% Rendimiento"
    ))
    fig3.update_traces(
        textposition="outside", texttemplate="%{y:.2f}%",
        textfont=dict(color="#1c1008", size=11, family="Georgia")
    )
    fig3.add_hline(
        y=100, line_dash="dash", line_color="#d4a96a",
        annotation_text="100% referencia",
        annotation_font=dict(color="#3e2005", size=12, family="Georgia")
    )
    st.plotly_chart(fig3, use_container_width=True)

# ── Tab 4 ────────────────────────────────────
with tab4:
    st.markdown(
        "<p class='grafica-subtitulo'>Comparación de flujos de entrada y salida del balance global</p>",
        unsafe_allow_html=True
    )
    df_balance = pd.DataFrame({
        "Flujo":     ["Pulpa (P)", "Miel (M)", "Azúcar (Az)", "Agua (A)",
                      "Vino (V)", "CO₂", "Sólidos (S)"],
        "kg/h":      [116500, 56000, 6500, 150000, 286046.9, 31303.1, 11650],
        "Dirección": ["Entrada","Entrada","Entrada","Entrada",
                      "Salida","Salida","Salida"]
    })
    fig4 = px.bar(
        df_balance, x="Flujo", y="kg/h",
        color="Dirección",
        color_discrete_map={"Entrada": "#c8922a", "Salida": "#3e2005"},
        text="kg/h",
        barmode="group"
    )
    fig4.update_layout(**hacer_layout(
        "Balance global: entradas vs salidas (kg/h)",
        label_x="Flujo", label_y="kg/h",
        angulo_x=-20,
        mostrar_leyenda=True
    ))
    fig4.update_traces(
        textposition="outside", texttemplate="%{y:,.0f}",
        textfont=dict(color="#1c1008", size=11, family="Georgia")
    )
    st.plotly_chart(fig4, use_container_width=True)


# ─────────────────────────────────────────────
# TABLA DE RENDIMIENTOS
# ─────────────────────────────────────────────
st.markdown("---")
st.subheader(" Pérdidas y Rendimientos por Etapa")
st.dataframe(df_rend, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
# NOTAS DE PRODUCCIÓN
# ─────────────────────────────────────────────
st.markdown("---")
st.subheader(" Notas de Producción")

col_n1, col_n2 = st.columns(2)

with col_n1:
    notas = st.text_area(
        "Observaciones del lote:",
        placeholder="Ej: Lote #001 - Iniciado el 20/05/2026. Temperatura: 22°C...",
        height=120
    )
    if notas:
        st.success(" Nota registrada correctamente")

with col_n2:
    fecha = st.date_input(" Fecha de inicio del lote")
    lote  = st.text_input(" Número de lote", placeholder="Ej: AURUM-001")
    st.info(f"Lote: **{lote if lote else '—'}** | Inicio: **{fecha}**")

st.markdown("---")
st.caption(" Aurum · Dashboard de Producción")
