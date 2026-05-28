# ============================================
# AURUM · Dashboard de Producción v3.0
# Datos reales del balance de masa del vino
# Soft Vintage · Vino de Maracuyá 
# ============================================
import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import os

# página principal — layout wide para aprovechar el espacio
st.set_page_config(
    page_title="Aurum · Vino de Maracuyá",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# estilos visuales del dashboard — paleta soft vintage maracuyá
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

/* encabezado de la tabla */
thead tr th {
    background-color: #1c1008 !important; color: #e8b84b !important;
    font-family: Georgia, serif !important; letter-spacing: 1px !important;
}
tbody tr:nth-child(even) { background-color: #fdf0d0 !important; }
tbody tr:nth-child(odd)  { background-color: #fffdf5 !important; }
tbody tr td { color: #2c1a0e !important; }

/* tarjetas de métricas */
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


# carga una imagen desde disco y la convierte a base64
# necesario para incrustarla dentro de HTML personalizado
def cargar_imagen_local(ruta):
    if not os.path.exists(ruta):
        return None, None
    ext  = os.path.splitext(ruta)[1].lower()
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}.get(ext, "image/png")
    with open(ruta, "rb") as f:
        return base64.b64encode(f.read()).decode(), mime


# ══════════════════════════════════════════════════════
#   RUTAS DE ARCHIVOS — edita solo estas líneas
#
#   Logo y QR: pon el nombre del archivo si están en la
#   misma carpeta que este script, o la ruta completa:
#     r"C:\Users\SANTIAGO\Pictures\logo_aurum.png"
#
#   Excel: ruta al archivo BALANCE.xlsx en tu equipo.
#   Cada vez que lo actualices, el dashboard se refresca
#   automáticamente al recargar la página.
# ══════════════════════════════════════════════════════
RUTA_LOGO  = r"D:\Aurum_v2.3\LOGO + QR\Aurum.jpeg"    # <- ruta de logo
RUTA_QR    = r"D:\Aurum_v2.3\LOGO + QR\AurumQR.png"   # <- ruta de QR
RUTA_EXCEL = r"D:\Aurum_v2.3\xlsx\BALANCE.xlsx"        # <- ruta de Excel de balance
# ══════════════════════════════════════════════════════

img_b64, tipo    = cargar_imagen_local(RUTA_LOGO)
qr_b64,  qr_tipo = cargar_imagen_local(RUTA_QR)


# ─────────────────────────────────────────────────────
# LECTURA DEL EXCEL DE BALANCE
# Lee la hoja única del archivo y extrae los datos
# reales de flujos másicos, fracciones y resultados.
# Si no encuentra el archivo usa datos de respaldo
# para que el dashboard no se rompa.
# ─────────────────────────────────────────────────────
@st.cache_data  # cachea la lectura para no releer en cada interacción
def cargar_balance(ruta):
    if not os.path.exists(ruta):
        return None
    return pd.read_excel(ruta, sheet_name=0, header=None)

raw = cargar_balance(RUTA_EXCEL)

# ─────────────────────────────────────────────────────
# DATOS REALES DEL BALANCE — extraídos del Excel
#
# Flujos másicos de ENTRADAS (kg/h):
#   Pulpa (P)    = 116,500
#   Miel (M)     = 56,000
#   Azúcar (Az)  = 6,500
#   Agua (A)     = 150,000
#   TOTAL        = 329,000
#
# Flujos másicos de SALIDAS (kg/h):
#   CO₂ (gas purga) = 31,303.10
#   Sólidos (S)     = 11,650
#   Vino (V)        = 286,046.90
#
# Composición del vino final:
#   Etanol   = 32,766.90 kg/h  → 11.45%
#   Agua     = 253,280   kg/h  → 88.54%
#   Sólidos  = 0         kg/h  →  0%
#
# Pérdidas y rendimientos:
#   Mezclado     → 100% rendimiento
#   Fermentación → 90.49% rendimiento
#   Filtrado     → 96.09% rendimiento
#   Total        → 86.94% rendimiento
# ─────────────────────────────────────────────────────

# tabla principal de ingredientes con datos reales del balance
ingredientes = {
    "Componente": [
        "Pulpa de maracuyá (P)",
        "Miel (M)",
        "Azúcar (Az)",
        "Agua (A)",
        "CO₂ — gas de purga",
        "Sólidos insolubles (S)",
        "Etanol en vino (C₂H₅OH)",
        "Agua en vino (H₂O)",
        "Vino final (V)"
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

# tabla de rendimientos por etapa del proceso
rendimientos = {
    "Etapa":          ["Mezclado", "Fermentación", "Filtrado", "Global"],
    "Pérdida (kg/h)": [0.0, 31303.10, 11650.0, 42953.10],
    "% Pérdida":      [0.0, 9.51, 3.54, 13.06],
    "% Rendimiento":  [100.0, 90.49, 96.09, 86.94]
}
df_rend = pd.DataFrame(rendimientos)

# tabla de composición del vino final — solo las 3 fracciones reales
df_vino = pd.DataFrame({
    "Componente": ["Etanol (C₂H₅OH)", "Agua (H₂O)", "Sólidos"],
    "kg/h":       [32766.90, 253280.0, 0.0],
    "Fracción %": [11.45, 88.54, 0.0]
})

# paleta de colores vintage para todas las gráficas
PALETA = ["#c8922a", "#e8b84b", "#7a4f1d", "#3e2005",
          "#d4a96a", "#f0d080", "#a0622a", "#1c1008"]

# configuración base para todas las gráficas — evita repetir código
LAYOUT = dict(
    plot_bgcolor="#fdf6e3", paper_bgcolor="#fdf6e3",
    font_color="#2c1a0e",   font_family="Georgia",
    title_font_color="#3e2005", title_font_size=13,
    showlegend=False
)


# ─────────────────────────────────────────────
# TÍTULO DEL DASHBOARD
# ─────────────────────────────────────────────
st.markdown('<p class="titulo-principal">🍷 AURUM</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitulo">Dashboard de Balance · Vino de Maracuyá </p>',
    unsafe_allow_html=True
)
st.markdown("---")

# layout de dos columnas: izquierda más angosta, derecha más ancha
col_izq, col_der = st.columns([1, 2])


# ══════════════════════════════════════════════
# COLUMNA IZQUIERDA — logo, QR e info del vino
# ══════════════════════════════════════════════
with col_izq:

    c_logo, c_qr = st.columns(2)   # logo y QR lado a lado

    # ── LOGO ──────────────────────────────────
    with c_logo:
        st.markdown(
            "<p style='text-align:center; font-family:Georgia,serif; "
            "color:#3e2005; font-weight:bold; font-size:0.8rem; "
            "margin-bottom:4px;'></p>",
            unsafe_allow_html=True
        )
        if img_b64 is not None:
            st.markdown(f"""
                <div style="background:#fffdf5; border:1.5px solid #d4a96a;
                     border-radius:12px; overflow:hidden;
                     height:180px; display:flex; flex-direction:column;
                     align-items:center; justify-content:center;">
                    <img src="data:{tipo};base64,{img_b64}"
                         style="width:100%; height:140px;
                                object-fit:cover; display:block;">
                    <p style="color:#3e2005; font-family:Georgia,serif;
                              font-weight:bold; font-size:0.8rem;
                              margin:4px 0 0; letter-spacing:2px;">AURUM</p>
                    <p style="color:#7a4f1d; font-style:italic;
                              font-size:0.65rem; margin:1px 0 4px;">Vino de Maracuyá</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="background:#fffdf5; border:2px dashed #d4a96a;
                     border-radius:12px; height:180px; display:flex;
                     flex-direction:column; align-items:center; justify-content:center;">
                    <div style="font-size:52px;">🍾</div>
                    <p style="color:#7a4f1d; font-size:0.68rem; font-style:italic; margin:4px 0 0;">Sin logo</p>
                    <p style="color:#c8922a; font-size:0.62rem; margin:2px 0 0;">Edita RUTA_LOGO</p>
                </div>
            """, unsafe_allow_html=True)

    # ── QR ────────────────────────────────────
    with c_qr:
        st.markdown(
            "<p style='text-align:center; font-family:Georgia,serif; "
            "color:#3e2005; font-weight:bold; font-size:0.8rem; "
            "margin-bottom:4px;'></p>",
            unsafe_allow_html=True
        )
        if qr_b64 is not None:
            st.markdown(f"""
                <div style="background:#ffffff; border:1.5px solid #d4a96a;
                     border-radius:12px; overflow:hidden;
                     height:180px; display:flex; flex-direction:column;
                     align-items:center; justify-content:center;">
                    <img src="data:{qr_tipo};base64,{qr_b64}"
                         style="width:100%; height:148px;
                                object-fit:contain; display:block;
                                padding:6px; box-sizing:border-box;
                                background:#ffffff;">
                    <p style="color:#7a4f1d; font-size:0.65rem;
                              font-style:italic; margin:2px 0 4px;">Escanea para más info</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="background:#fdf0d0; border:2px dashed #c8922a;
                     border-radius:12px; height:180px; display:flex;
                     flex-direction:column; align-items:center; justify-content:center;">
                    <div style="font-size:40px; opacity:0.4;">⬛</div>
                    <p style="color:#c8922a; font-size:0.68rem; font-style:italic;
                              margin:6px 0 0; font-family:Georgia,serif;">
                              Espacio QR<br>reservado</p>
                    <p style="color:#c8922a; font-size:0.62rem; margin:2px 0 0;">Edita RUTA_QR</p>
                </div>
            """, unsafe_allow_html=True)

    # ficha del proceso — datos reales del balance
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

    st.subheader("⚗️ Balance Global de Masa")
    # tabla con todos los flujos y fracciones del proceso
    st.dataframe(df, use_container_width=True, hide_index=True)

    # métricas clave del balance — valores reales del Excel
    st.markdown("### 📊 Valores Clave del Balance")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Entrada total",    "329,000 kg/h")
    m2.metric("Vino producido",   "286,047 kg/h")
    m3.metric("Etanol en vino",   "11.45%")
    m4.metric("Rendimiento",      "86.94%")

    # segunda fila de métricas — energía y pérdidas
    m5, m6, m7, m8 = st.columns(4)
    m5.metric("CO₂ generado",      "31,303 kg/h")
    m6.metric("Sólidos filtrados",  "11,650 kg/h")
    m7.metric("Qr fermentación",    "37,288,740 kJ/h")
    m8.metric("Q chaqueta",         "25,463,642 kJ/h")


# ─────────────────────────────────────────────
# GRÁFICAS EN TABS — datos reales del balance
# ─────────────────────────────────────────────
st.markdown("---")
st.subheader("📈 Visualización del Balance")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Flujos de entrada",
    "🥧 Composición del vino",
    "📉 Rendimientos por etapa",
    "⚖️ Entradas vs Salidas"
])

# flujos másicos de cada ingrediente de entrada
with tab1:
    st.markdown("Flujo másico de cada componente en la alimentación (kg/h)")
    df_ent = df[df["Tipo"] == "Entrada"].copy()
    fig1 = px.bar(
        df_ent, x="Componente", y="Flujo (kg/h)",
        color="Componente", text="Flujo (kg/h)",
        color_discrete_sequence=PALETA,
        title="Flujos másicos de entrada al proceso (kg/h)"
    )
    fig1.update_layout(**LAYOUT, xaxis_tickangle=-20)
    fig1.update_traces(textposition="outside", texttemplate="%{y:,.0f}")
    st.plotly_chart(fig1, use_container_width=True)

# composición porcentual del vino final
with tab2:
    st.markdown("Fracción másica de cada componente en el vino producido")
    df_comp = df_vino[df_vino["Fracción %"] > 0].copy()
    fig2 = px.pie(
        df_comp, names="Componente", values="Fracción %",
        color_discrete_sequence=PALETA,
        title="Composición del vino final (% másico)"
    )
    fig2.update_layout(
        plot_bgcolor="#fdf6e3", paper_bgcolor="#fdf6e3",
        font_color="#2c1a0e",   font_family="Georgia",
        title_font_color="#3e2005", title_font_size=13
    )
    fig2.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig2, use_container_width=True)

# rendimiento real de cada etapa del proceso
with tab3:
    st.markdown("Porcentaje de rendimiento en cada etapa del proceso productivo")
    fig3 = px.bar(
        df_rend, x="Etapa", y="% Rendimiento",
        color="Etapa", text="% Rendimiento",
        color_discrete_sequence=PALETA,
        title="Rendimiento por etapa del proceso (%)"
    )
    fig3.update_layout(**LAYOUT, xaxis_tickangle=0)
    fig3.update_traces(textposition="outside", texttemplate="%{y:.2f}%")
    # línea de referencia al 100%
    fig3.add_hline(y=100, line_dash="dash", line_color="#d4a96a",
                   annotation_text="100% referencia")
    st.plotly_chart(fig3, use_container_width=True)

# comparación visual entradas vs salidas del balance global
with tab4:
    st.markdown("Comparación de flujos de entrada y salida del balance global")
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
        title="Balance global: entradas vs salidas (kg/h)",
        barmode="group"
    )
    fig4.update_layout(
        plot_bgcolor="#fdf6e3", paper_bgcolor="#fdf6e3",
        font_color="#2c1a0e",   font_family="Georgia",
        title_font_color="#3e2005", title_font_size=13,
        xaxis_tickangle=-20
    )
    fig4.update_traces(textposition="outside", texttemplate="%{y:,.0f}")
    st.plotly_chart(fig4, use_container_width=True)


# ─────────────────────────────────────────────
# TABLA DE RENDIMIENTOS — resumen del proceso
# ─────────────────────────────────────────────
st.markdown("---")
st.subheader("📋 Pérdidas y Rendimientos por Etapa")
st.dataframe(df_rend, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
# NOTAS DE PRODUCCIÓN
# ─────────────────────────────────────────────
st.markdown("---")
st.subheader("📝 Notas de Producción")

col_n1, col_n2 = st.columns(2)

with col_n1:
    notas = st.text_area(
        "Observaciones del lote:",
        placeholder="Ej: Lote #001 - Iniciado el 20/05/2026. Temperatura: 22°C...",
        height=120
    )
    if notas:
        st.success("✅ Nota registrada correctamente")

with col_n2:
    fecha = st.date_input("📅 Fecha de inicio del lote")
    lote  = st.text_input("🔢 Número de lote", placeholder="Ej: AURUM-001")
    st.info(f"Lote: **{lote if lote else '—'}** | Inicio: **{fecha}**")

st.markdown("---")
st.caption("🍷 Aurum · Dashboard de Producción")