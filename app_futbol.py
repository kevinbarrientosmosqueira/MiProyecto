import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.colors as pc

# ──────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ──────────────────────────────────────────────

st.set_page_config(
    page_title="Proyecto de Análisis de Jugadores de Fútbol",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────
# ESTILO PERSONALIZADO
# ──────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
}

.stApp {
    background: #f5faf7;
}

/* ── Hero header ── */
.hero-wrap {
    background: #ffffff;
    border-radius: 0px;
    padding: 3rem 2.5rem 2.5rem;
    margin-bottom: 2.5rem;
    border-bottom: 4px solid #1e8c4d;
}
.main-header {
    color: #0d3320;
    font-size: 3rem;
    font-weight: 800;
    letter-spacing: -1.5px;
    margin-bottom: 0.4rem;
    line-height: 1.1;
}
.sub-header {
    color: #27ae60;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.hero-desc {
    color: #3a5a45;
    font-size: 0.95rem;
    max-width: 680px;
    line-height: 1.8;
    margin-top: 0.6rem;
}

/* ── Títulos de sección ── */
.section-title {
    color: #0d3320;
    font-size: 2rem;
    font-weight: 800;
    margin-top: 1.2rem;
    margin-bottom: 0.3rem;
    letter-spacing: -0.5px;
    border-left: 6px solid #27ae60;
    padding-left: 1rem;
    line-height: 1.2;
}
.section-subtitle {
    color: #4a7a5a;
    font-size: 0.85rem;
    margin-bottom: 1.2rem;
    padding-left: 1.5rem;
    font-weight: 400;
    letter-spacing: 0.3px;
}

/* ── Sub-títulos ── */
.subsection-title {
    color: #0d3320;
    font-size: 1.3rem;
    font-weight: 700;
    margin-top: 1.5rem;
    margin-bottom: 0.6rem;
    border-bottom: 2px solid #c8e8d4;
    padding-bottom: 0.4rem;
}

/* ── Cuadros informativos ── */
.info-box {
    background: #ffffff;
    border-left: 5px solid #27ae60;
    border-radius: 0 10px 10px 0;
    padding: 1rem 1.4rem;
    margin-bottom: 1.4rem;
    color: #1a3a2a;
    font-size: 0.92rem;
    line-height: 1.85;
    box-shadow: 0 1px 6px rgba(39,174,96,0.08);
}
.info-box strong { color: #0d5c2f; }

/* ── Métricas en lista vertical ── */
.metric-list {
    background: #ffffff;
    border: 1px solid #c8e8d4;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.4rem;
    box-shadow: 0 2px 10px rgba(39,174,96,0.06);
}
.metric-row {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    padding: 0.7rem 0;
    border-bottom: 1px solid #e8f5ec;
}
.metric-row:last-child {
    border-bottom: none;
}
.metric-row-label {
    color: #3a6a4a;
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.2px;
}
.metric-row-value {
    color: #0d3320;
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.25rem;
    font-weight: 700;
}
.metric-row-sub {
    color: #6a9a7a;
    font-size: 0.78rem;
    margin-top: 0.1rem;
    text-align: right;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #e6f2ea;
    border-radius: 10px;
    gap: 3px;
    padding: 3px;
}
.stTabs [data-baseweb="tab"] {
    color: #2a5a3a;
    border-radius: 7px;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: .3px;
}
.stTabs [aria-selected="true"] {
    background: #27ae60 !important;
    color: #ffffff !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #c8e8d4;
}

/* ── Botón descarga ── */
.stDownloadButton > button {
    background: #27ae60;
    color: #ffffff;
    font-weight: 700;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.4rem;
    font-size: 0.9rem;
    letter-spacing: 0.3px;
    font-family: 'Sora', sans-serif;
}
.stDownloadButton > button:hover {
    background: #1e8c4d;
    color: #ffffff;
}

hr { border-color: #c8e8d4; margin: 2.2rem 0; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# LAYOUT PLOTLY BASE
# ──────────────────────────────────────────────

BASE_LAYOUT = dict(
    paper_bgcolor="rgba(255,255,255,0)",
    plot_bgcolor="rgba(255,255,255,0)",
    font=dict(family="Sora, sans-serif", color="#1a3a2a", size=12),
    title_font=dict(color="#0d3320", size=14, family="Sora, sans-serif"),
    xaxis=dict(gridcolor="#ddeee5", zerolinecolor="#b8ddc8", color="#1a3a2a"),
    yaxis=dict(gridcolor="#ddeee5", zerolinecolor="#b8ddc8", color="#1a3a2a"),
    margin=dict(l=20, r=20, t=55, b=35),
    legend=dict(bgcolor="rgba(255,255,255,0.85)", font=dict(color="#1a3a2a")),
)

VERDE_SCALE = [
    "#c8f0d5", "#9addb5", "#6bc895", "#3db377",
    "#27ae60", "#1e8c4d", "#156b3a", "#0d4a27",
]

# ──────────────────────────────────────────────
# CARGA DE DATOS
# ──────────────────────────────────────────────

@st.cache_data
def cargar_datos(path: str = "futbol.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"jugador", "equipo", "goles"}
    if not required.issubset(df.columns):
        st.error(f"El CSV debe contener al menos: {required}")
        st.stop()
    df = df.dropna(subset=["jugador", "equipo", "goles"])
    df["goles"] = pd.to_numeric(df["goles"], errors="coerce")
    df = df.dropna(subset=["goles"])
    df["goles"] = df["goles"].astype(int)
    return df.reset_index(drop=True)

df = cargar_datos()

# ──────────────────────────────────────────────
# HELPER: tabla de frecuencias
# ──────────────────────────────────────────────

def tabla_frecuencias(serie: pd.Series, labels: list, bins) -> pd.DataFrame:
    cats = pd.cut(serie, bins=bins, labels=labels, right=False, include_lowest=True)
    fi = cats.value_counts().reindex(labels, fill_value=0)

    midpoints = []
    for i in range(len(bins) - 1):
        lo = bins[i]
        hi_ = bins[i + 1]
        if hi_ == np.inf:
            hi_ = lo * 1.5 if lo > 0 else lo + 20
        midpoints.append(round((lo + hi_) / 2, 2))

    tf = pd.DataFrame({
        "Intervalo":      labels,
        "Marca de clase": midpoints,
        "fi":             fi.values,
    })
    total = tf["fi"].sum()
    tf["hi"]  = (tf["fi"] / total).round(4)
    tf["hi%"] = (tf["hi"] * 100).round(2)
    tf["Fi"]  = tf["fi"].cumsum()
    tf["Hi"]  = tf["hi"].cumsum().round(4)

    fila_total = pd.DataFrame([{
        "Intervalo":      "TOTAL",
        "Marca de clase": "—",
        "fi":  tf["fi"].sum(),
        "hi":  round(tf["hi"].sum(), 4),
        "hi%": round(tf["hi%"].sum(), 2),
        "Fi":  tf["Fi"].iloc[-1],
        "Hi":  round(tf["Hi"].iloc[-1], 4),
    }])
    return pd.concat([tf, fila_total], ignore_index=True)


# ──────────────────────────────────────────────
# INTERVALOS DE GOLES
# ──────────────────────────────────────────────

GOLES_BINS   = [0, 5, 10, 15, 20, 25, 30, np.inf]
GOLES_LABELS = [
    "0 – 4",
    "5 – 9",
    "10 – 14",
    "15 – 19",
    "20 – 24",
    "25 – 29",
    "≥ 30",
]

df["cat_goles"] = pd.cut(
    df["goles"], bins=GOLES_BINS, labels=GOLES_LABELS, right=False, include_lowest=True
)

# ──────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────

st.markdown("""
<div class="hero-wrap">
    <p class="sub-header">Proyecto de Análisis de Jugadores de Fútbol</p>
    <p class="hero-desc">
        📊 Este dashboard presenta un análisis estadístico completo de dos variables clave del dataset:
        el <strong>equipo</strong> al que pertenece cada jugador (variable cualitativa nominal)
        y la cantidad de <strong>goles anotados</strong> durante la temporada (variable cuantitativa discreta).
        Para cada variable se construye una tabla de frecuencias con todos sus componentes,
        acompañada de visualizaciones gráficas que facilitan la interpretación de los datos.
        Los datos son ficticios y tienen fines exclusivamente académicos.
    </p>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# DATASET — DESCARGA Y PREVISUALIZACIÓN
# ──────────────────────────────────────────────

st.markdown('<p class="section-title">📁 Dataset</p>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">Archivo fuente · futbol.csv</p>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    📌 <strong>Sobre los datos:</strong> El archivo CSV contiene la información de todos los jugadores
    analizados en este estudio. Cada fila representa un jugador con sus atributos: nombre, equipo,
    edad, goles anotados, asistencias y valor de mercado estimado. Podés descargar el archivo
    original o explorar una vista previa de los primeros registros a continuación.
</div>
""", unsafe_allow_html=True)

# Botón de descarga
with open("futbol.csv", "rb") as f:
    csv_bytes = f.read()

st.download_button(
    label="⬇️ Descargar futbol.csv",
    data=csv_bytes,
    file_name="futbol.csv",
    mime="text/csv",
)

# Previsualización del dataset
st.markdown('<p class="subsection-title">🔍 Vista previa del archivo (primeros 8 registros)</p>', unsafe_allow_html=True)

cols_mostrar = [c for c in ["jugador", "equipo", "edad", "goles", "asistencias", "valor_millones"] if c in df.columns]
tabla_vista = df[cols_mostrar].head(8).copy()
rename_map = {
    "jugador": "Jugador", "equipo": "Equipo", "edad": "Edad",
    "goles": "Goles", "asistencias": "Asistencias", "valor_millones": "Valor (M€)"
}
tabla_vista.columns = [rename_map.get(c, c) for c in tabla_vista.columns]

col_config_prev = {
    "Jugador":    st.column_config.TextColumn(width="medium"),
    "Equipo":     st.column_config.TextColumn(width="medium"),
}
if "Goles" in tabla_vista.columns:
    col_config_prev["Goles"] = st.column_config.NumberColumn(format="%d")
if "Asistencias" in tabla_vista.columns:
    col_config_prev["Asistencias"] = st.column_config.NumberColumn(format="%d")
if "Valor (M€)" in tabla_vista.columns:
    col_config_prev["Valor (M€)"] = st.column_config.NumberColumn(format="%.0f M€")

st.dataframe(tabla_vista, use_container_width=True, hide_index=True,
             height=310, column_config=col_config_prev)

st.caption(f"📋 Mostrando 8 de {len(df)} jugadores en total.")

st.divider()

# ══════════════════════════════════════════════
# ANÁLISIS DE EQUIPOS
# ══════════════════════════════════════════════

st.markdown('<p class="section-title">🏟️ Análisis de Equipos</p>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">Variable cualitativa nominal · Distribución de jugadores por club</p>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    🏷️ <strong>Variable cualitativa nominal — Equipo:</strong><br>
    Se analiza a qué club pertenece cada jugador del dataset. Al tratarse de una variable cualitativa,
    los valores posibles son nombres de equipos (categorías sin orden numérico). Por este motivo,
    la <em>marca de clase</em> no es aplicable aquí; en su lugar se trabaja directamente con los nombres de cada club.<br><br>
    📐 Se calculan la <strong>frecuencia absoluta (fi)</strong> —cuántos jugadores hay por equipo—,
    la <strong>frecuencia relativa (hi)</strong> —qué proporción representa cada club sobre el total—,
    y las respectivas <strong>frecuencias acumuladas (Fi, Hi)</strong>. La tabla está ordenada de mayor
    a menor representación para facilitar la lectura.
</div>
""", unsafe_allow_html=True)

# Frecuencias de equipos
eq_fi   = df["equipo"].value_counts().reset_index()
eq_fi.columns = ["Equipo", "fi"]
eq_fi   = eq_fi.sort_values("fi", ascending=False).reset_index(drop=True)
total_j = len(df)
eq_fi["hi"]  = (eq_fi["fi"] / total_j).round(4)
eq_fi["hi%"] = (eq_fi["hi"] * 100).round(2)
eq_fi["Fi"]  = eq_fi["fi"].cumsum()
eq_fi["Hi"]  = eq_fi["hi"].cumsum().round(4)

fila_total_eq = pd.DataFrame([{
    "Equipo": "TOTAL", "fi": total_j,
    "hi": round(eq_fi["hi"].sum(), 4),
    "hi%": round(eq_fi["hi%"].sum(), 2),
    "Fi": eq_fi["Fi"].iloc[-1],
    "Hi": round(eq_fi["Hi"].iloc[-1], 4),
}])
eq_tabla = pd.concat([eq_fi, fila_total_eq], ignore_index=True)

# ── Métricas de equipos en lista vertical ──
equipo_max = eq_fi.iloc[0]
equipo_min = eq_fi.iloc[-1]

st.markdown('<p class="subsection-title">📌 Resumen de métricas — Equipos</p>', unsafe_allow_html=True)

st.markdown(f"""
<div class="metric-list">
    <div class="metric-row">
        <div>
            <div class="metric-row-label">👥 Total de jugadores en el dataset</div>
            <div class="metric-row-sub">Suma de todos los registros válidos</div>
        </div>
        <div class="metric-row-value">{total_j}</div>
    </div>
    <div class="metric-row">
        <div>
            <div class="metric-row-label">🏟️ Cantidad de equipos distintos</div>
            <div class="metric-row-sub">Número de categorías únicas</div>
        </div>
        <div class="metric-row-value">{df['equipo'].nunique()}</div>
    </div>
    <div class="metric-row">
        <div>
            <div class="metric-row-label">🥇 Club más representado</div>
            <div class="metric-row-sub">{equipo_max['Equipo']}</div>
        </div>
        <div class="metric-row-value">{equipo_max['fi']} jugadores</div>
    </div>
    <div class="metric-row">
        <div>
            <div class="metric-row-label">📉 Club menos representado</div>
            <div class="metric-row-sub">{equipo_min['Equipo']}</div>
        </div>
        <div class="metric-row-value">{equipo_min['fi']} jugadores</div>
    </div>
    <div class="metric-row">
        <div>
            <div class="metric-row-label">📊 Promedio de jugadores por equipo</div>
            <div class="metric-row-sub">fi promedio entre todos los clubes</div>
        </div>
        <div class="metric-row-value">{eq_fi['fi'].mean():.1f}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Tabla de frecuencias de equipos ──
st.markdown('<p class="subsection-title">📋 Tabla de Frecuencias — Equipos</p>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    📖 <strong>Cómo leer esta tabla:</strong><br>
    · <strong>fi</strong> = frecuencia absoluta → cuántos jugadores pertenecen a ese equipo.<br>
    · <strong>hi</strong> = frecuencia relativa → proporción del club sobre el total (entre 0 y 1).<br>
    · <strong>hi%</strong> = frecuencia relativa porcentual → lo mismo expresado en porcentaje.<br>
    · <strong>Fi</strong> = frecuencia absoluta acumulada → suma progresiva de jugadores hasta esa fila.<br>
    · <strong>Hi</strong> = frecuencia relativa acumulada → proporción acumulada hasta esa fila.<br>
    La tabla está ordenada de mayor a menor cantidad de jugadores por equipo.
</div>
""", unsafe_allow_html=True)

st.dataframe(eq_tabla, use_container_width=True, hide_index=True,
    column_config={
        "Equipo": st.column_config.TextColumn(width="medium"),
        "fi":  st.column_config.NumberColumn("fi",  format="%d"),
        "Fi":  st.column_config.NumberColumn("Fi",  format="%d"),
        "hi":  st.column_config.NumberColumn("hi",  format="%.4f"),
        "Hi":  st.column_config.NumberColumn("Hi",  format="%.4f"),
        "hi%": st.column_config.NumberColumn("hi%", format="%.2f%%"),
    }
)

# ── Gráficos de equipos ──
st.markdown('<p class="subsection-title">📊 Gráficos — Equipos</p>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    📈 <strong>Sobre los gráficos:</strong> Al ser una variable cualitativa, se utilizan cuatro tipos de representación gráfica.<br>
    · <strong>Barras</strong>: ideal para comparar visualmente la frecuencia de cada equipo de un vistazo.<br>
    · <strong>Bastones</strong>: similar a las barras pero con líneas, resaltando los puntos discretos de cada categoría.<br>
    · <strong>Torta</strong>: muestra la proporción porcentual de cada club sobre el total del dataset.<br>
    · <strong>Ojiva</strong>: curva de frecuencias acumuladas; permite leer cuántos jugadores pertenecen a los N equipos con más representación.
</div>
""", unsafe_allow_html=True)

eq_data = eq_fi.copy()
n_eq    = len(eq_data)
verde_colores = pc.sample_colorscale(
    "Greens", [i / max(n_eq - 1, 1) for i in range(n_eq)]
)
verde_colores_rev = list(reversed(verde_colores))

tab_e1, tab_e2, tab_e3, tab_e4 = st.tabs([
    "📊 Barras",
    "🎯 Bastones",
    "🥧 Torta",
    "📈 Ojiva",
])

with tab_e1:
    fig = go.Figure(go.Bar(
        x=eq_data["Equipo"],
        y=eq_data["fi"],
        marker=dict(
            color=verde_colores_rev,
            line=dict(color="#27ae60", width=0.8),
        ),
        text=eq_data["fi"],
        textposition="outside",
        textfont=dict(color="#0d3320", size=11),
    ))
    fig.update_layout(
        **BASE_LAYOUT,
        title="Número de jugadores por equipo",
        xaxis_tickangle=-20,
        height=420,
        xaxis_title="Equipo",
        yaxis_title="Jugadores (fi)",
    )
    st.plotly_chart(fig, use_container_width=True)

with tab_e2:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=eq_data["Equipo"], y=eq_data["fi"],
        mode="markers+lines",
        marker=dict(color="#27ae60", size=11, symbol="circle"),
        line=dict(color="#27ae60", width=1, dash="dot"),
    ))
    for _, row in eq_data.iterrows():
        fig.add_shape(
            type="line",
            x0=row["Equipo"], x1=row["Equipo"],
            y0=0, y1=row["fi"],
            line=dict(color="#1e8c4d", width=2.5),
        )
    fig.update_layout(
        **BASE_LAYOUT,
        title="Diagrama de bastones — Frecuencia absoluta por equipo",
        xaxis_tickangle=-20,
        height=420,
        xaxis_title="Equipo",
        yaxis_title="fi",
    )
    st.plotly_chart(fig, use_container_width=True)

with tab_e3:
    fig = go.Figure(go.Pie(
        labels=eq_data["Equipo"],
        values=eq_data["fi"],
        marker=dict(colors=verde_colores_rev),
        hole=0.38,
        textposition="inside",
        textinfo="percent+label",
        textfont=dict(size=11, color="#0d3320"),
    ))
    fig.update_layout(
        **BASE_LAYOUT,
        height=460,
        title="Distribución porcentual de jugadores por equipo",
    )
    st.plotly_chart(fig, use_container_width=True)

with tab_e4:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=eq_data["Equipo"],
        y=eq_data["Fi"],
        mode="lines+markers",
        marker=dict(color="#27ae60", size=9, symbol="square"),
        line=dict(color="#1e8c4d", width=2),
        fill="tozeroy",
        fillcolor="rgba(39,174,96,0.08)",
        name="Ojiva (Fi)",
    ))
    fig.update_layout(
        **BASE_LAYOUT,
        title="Ojiva — Frecuencia acumulada de jugadores por equipo",
        xaxis_tickangle=-20,
        height=420,
        xaxis_title="Equipo",
        yaxis_title="Fi (acumulada)",
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ══════════════════════════════════════════════
# ANÁLISIS DE GOLES
# ══════════════════════════════════════════════

st.markdown('<p class="section-title">🥅 Análisis de Goles</p>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">Variable cuantitativa discreta · Goles anotados por jugador en la temporada</p>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    🔢 <strong>Variable cuantitativa discreta — Goles anotados:</strong><br>
    Los goles son valores numéricos enteros que se pueden contar individualmente. Para construir la
    tabla de frecuencias, los jugadores se agrupan en <strong>7 intervalos de 5 goles cada uno</strong>
    (excepto el último, que es abierto hacia arriba: ≥ 30 goles).<br><br>
    📏 La <strong>marca de clase</strong> es el punto medio de cada intervalo y representa el valor típico
    del grupo. Por ejemplo, para el intervalo <em>10 – 14</em>, la marca de clase es <strong>12</strong>.
    Este valor se usa en estadística para calcular la media ponderada cuando solo se dispone de datos agrupados.<br><br>
    📐 También se calculan medidas de tendencia central (media, mediana) y de dispersión
    (desviación estándar) para describir el comportamiento general de la distribución de goles.
</div>
""", unsafe_allow_html=True)

# ── Métricas de goles en lista vertical ──
goles_vals = df["goles"]
idx_max = goles_vals.idxmax()
idx_min = goles_vals.idxmin()

st.markdown('<p class="subsection-title">📌 Resumen de métricas — Goles</p>', unsafe_allow_html=True)

st.markdown(f"""
<div class="metric-list">
    <div class="metric-row">
        <div>
            <div class="metric-row-label">📊 Media aritmética</div>
            <div class="metric-row-sub">Promedio de goles por jugador en la temporada</div>
        </div>
        <div class="metric-row-value">{goles_vals.mean():.2f} goles</div>
    </div>
    <div class="metric-row">
        <div>
            <div class="metric-row-label">📍 Mediana</div>
            <div class="metric-row-sub">Valor central: el 50% de los jugadores anotó menos que este número</div>
        </div>
        <div class="metric-row-value">{goles_vals.median():.1f} goles</div>
    </div>
    <div class="metric-row">
        <div>
            <div class="metric-row-label">🎯 Moda</div>
            <div class="metric-row-sub">Cantidad de goles que más se repite entre los jugadores</div>
        </div>
        <div class="metric-row-value">{int(goles_vals.mode().iloc[0])} goles</div>
    </div>
    <div class="metric-row">
        <div>
            <div class="metric-row-label">📐 Desviación estándar</div>
            <div class="metric-row-sub">Dispersión promedio respecto a la media — cuánto varía el rendimiento goleador</div>
        </div>
        <div class="metric-row-value">{goles_vals.std():.2f}</div>
    </div>
    <div class="metric-row">
        <div>
            <div class="metric-row-label">📦 Varianza</div>
            <div class="metric-row-sub">Cuadrado de la desviación estándar</div>
        </div>
        <div class="metric-row-value">{goles_vals.var():.2f}</div>
    </div>
    <div class="metric-row">
        <div>
            <div class="metric-row-label">📏 Rango</div>
            <div class="metric-row-sub">Diferencia entre el máximo y el mínimo goleador</div>
        </div>
        <div class="metric-row-value">{goles_vals.max() - goles_vals.min()} goles</div>
    </div>
    <div class="metric-row">
        <div>
            <div class="metric-row-label">🏆 Máximo goleador</div>
            <div class="metric-row-sub">{df.loc[idx_max, 'jugador']}</div>
        </div>
        <div class="metric-row-value">{goles_vals.max()} goles</div>
    </div>
    <div class="metric-row">
        <div>
            <div class="metric-row-label">📉 Mínimo goleador</div>
            <div class="metric-row-sub">{df.loc[idx_min, 'jugador']}</div>
        </div>
        <div class="metric-row-value">{goles_vals.min()} goles</div>
    </div>
    <div class="metric-row">
        <div>
            <div class="metric-row-label">🔢 Total de jugadores analizados</div>
            <div class="metric-row-sub">Registros válidos en el dataset</div>
        </div>
        <div class="metric-row-value">{len(goles_vals)}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Tabla de frecuencias de goles ──
st.markdown('<p class="subsection-title">📋 Tabla de Frecuencias — Goles (datos agrupados)</p>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    📖 <strong>Cómo leer esta tabla:</strong><br>
    · <strong>Intervalo</strong> = rango de goles que agrupa a jugadores con rendimiento similar.<br>
    · <strong>Marca de clase</strong> = punto medio del intervalo; valor representativo del grupo para cálculos estadísticos.<br>
    · <strong>fi</strong> = cantidad de jugadores en ese intervalo (frecuencia absoluta).<br>
    · <strong>hi</strong> = proporción de jugadores en ese intervalo sobre el total (frecuencia relativa).<br>
    · <strong>hi%</strong> = lo mismo expresado en porcentaje.<br>
    · <strong>Fi</strong> = cuántos jugadores acumulados anotaron hasta ese intervalo inclusive.<br>
    · <strong>Hi</strong> = proporción acumulada hasta ese intervalo.<br><br>
    ⚠️ El último intervalo (≥ 30) es abierto; su marca de clase se estimó aproximadamente.
</div>
""", unsafe_allow_html=True)

tf_goles = tabla_frecuencias(df["goles"], GOLES_LABELS, GOLES_BINS)
tf_goles_display = pd.concat([
    tf_goles[tf_goles["Intervalo"] != "TOTAL"].iloc[::-1].reset_index(drop=True),
    tf_goles[tf_goles["Intervalo"] == "TOTAL"],
], ignore_index=True)

st.dataframe(tf_goles_display, use_container_width=True, hide_index=True,
    column_config={
        "fi":  st.column_config.NumberColumn("fi",  format="%d"),
        "Fi":  st.column_config.NumberColumn("Fi",  format="%d"),
        "hi":  st.column_config.NumberColumn("hi",  format="%.4f"),
        "Hi":  st.column_config.NumberColumn("Hi",  format="%.4f"),
        "hi%": st.column_config.NumberColumn("hi%", format="%.2f%%"),
        "Marca de clase": st.column_config.NumberColumn(format="%.2f"),
    }
)

# ── Gráficos de goles ──
st.markdown('<p class="subsection-title">📊 Gráficos — Distribución de goles por intervalos</p>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    📈 <strong>Sobre los gráficos de goles:</strong><br>
    · <strong>Barras</strong>: muestra cuántos jugadores caen en cada intervalo de goles; es el histograma para datos agrupados.<br>
    · <strong>Bastones</strong>: igual que las barras pero en formato de líneas verticales; útil para ver la forma de la distribución.<br>
    · <strong>Torta</strong>: visualiza qué porcentaje del total representa cada intervalo de rendimiento goleador.<br>
    · <strong>Ojiva</strong>: curva de acumulación; permite leer, por ejemplo, "¿qué porcentaje de jugadores anotó menos de 15 goles?"
</div>
""", unsafe_allow_html=True)

tf_g_data     = tf_goles[tf_goles["Intervalo"] != "TOTAL"].copy()
tf_g_data_rev = tf_g_data.iloc[::-1].reset_index(drop=True)

n_g = len(tf_g_data_rev)
verde_g = pc.sample_colorscale("Greens", [i / max(n_g - 1, 1) for i in range(n_g)])
verde_g_rev = list(reversed(verde_g))

tab_g1, tab_g2, tab_g3, tab_g4 = st.tabs([
    "📊 Barras",
    "🎯 Bastones",
    "🥧 Torta",
    "📈 Ojiva",
])

with tab_g1:
    fig = go.Figure(go.Bar(
        x=tf_g_data_rev["Intervalo"],
        y=tf_g_data_rev["fi"],
        marker=dict(
            color=verde_g_rev,
            line=dict(color="#27ae60", width=0.8),
        ),
        text=tf_g_data_rev["fi"],
        textposition="outside",
        textfont=dict(color="#0d3320", size=11),
    ))
    fig.update_layout(
        **BASE_LAYOUT,
        title="Jugadores por intervalo de goles anotados",
        xaxis_tickangle=-10,
        height=420,
        xaxis_title="Intervalo de goles",
        yaxis_title="Número de jugadores (fi)",
    )
    st.plotly_chart(fig, use_container_width=True)

with tab_g2:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=tf_g_data_rev["Intervalo"], y=tf_g_data_rev["fi"],
        mode="markers+lines",
        marker=dict(color="#27ae60", size=11, symbol="circle"),
        line=dict(color="#27ae60", width=1, dash="dot"),
    ))
    for _, row in tf_g_data_rev.iterrows():
        fig.add_shape(
            type="line",
            x0=row["Intervalo"], x1=row["Intervalo"],
            y0=0, y1=row["fi"],
            line=dict(color="#1e8c4d", width=2.5),
        )
    fig.update_layout(
        **BASE_LAYOUT,
        title="Diagrama de bastones — Frecuencia absoluta de goles",
        xaxis_tickangle=-10,
        height=420,
        xaxis_title="Intervalo de goles",
        yaxis_title="fi",
    )
    st.plotly_chart(fig, use_container_width=True)

with tab_g3:
    fig = go.Figure(go.Pie(
        labels=tf_g_data_rev["Intervalo"],
        values=tf_g_data_rev["fi"],
        marker=dict(colors=verde_g_rev),
        hole=0.38,
        textposition="inside",
        textinfo="percent+label",
        textfont=dict(size=11, color="#0d3320"),
    ))
    fig.update_layout(
        **BASE_LAYOUT,
        height=460,
        title="Distribución porcentual de jugadores por rango de goles",
    )
    st.plotly_chart(fig, use_container_width=True)

with tab_g4:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=tf_g_data["Intervalo"],
        y=tf_g_data["Fi"],
        mode="lines+markers",
        marker=dict(color="#27ae60", size=9, symbol="square"),
        line=dict(color="#1e8c4d", width=2),
        fill="tozeroy",
        fillcolor="rgba(39,174,96,0.08)",
        name="Ojiva (Fi)",
    ))
    fig.update_layout(
        **BASE_LAYOUT,
        title="Ojiva — Frecuencia acumulada de goles (Fi)",
        xaxis_tickangle=-10,
        height=420,
        xaxis_title="Intervalo de goles",
        yaxis_title="Fi (acumulada)",
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Goles por jugador (ranking individual) ──
st.markdown('<p class="subsection-title">🏅 Ranking individual de goleadores</p>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    🎽 <strong>Rendimiento individual:</strong> Esta sección muestra los goles de cada jugador de forma directa,
    sin agrupar en intervalos. Los gráficos están ordenados de mayor a menor cantidad de goles anotados,
    lo que permite identificar rápidamente a los líderes de la tabla goleadora y observar cómo se
    distribuye el rendimiento individual a lo largo de toda la plantilla del dataset.<br><br>
    📊 El gráfico de la derecha muestra los <strong>goles totales acumulados por equipo</strong>,
    es decir, la suma de goles de todos los jugadores de cada club. Esto permite ver qué equipos
    aportan más producción ofensiva al conjunto de datos.
</div>
""", unsafe_allow_html=True)

df_sorted = df.sort_values("goles", ascending=False).reset_index(drop=True)
n_j = len(df_sorted)
colores_rank = pc.sample_colorscale("Greens", [i / max(n_j - 1, 1) for i in range(n_j)])
colores_rank_rev = list(reversed(colores_rank))

col_rank, col_eq_g = st.columns([3, 2])

with col_rank:
    fig = go.Figure(go.Bar(
        x=df_sorted["jugador"],
        y=df_sorted["goles"],
        marker=dict(color=colores_rank_rev, line=dict(color="#27ae60", width=0.6)),
        text=df_sorted["goles"],
        textposition="outside",
        textfont=dict(color="#0d3320", size=10),
        customdata=df_sorted["equipo"],
        hovertemplate="<b>%{x}</b><br>Goles: %{y}<br>Equipo: %{customdata}<extra></extra>",
    ))
    fig.update_layout(
        **BASE_LAYOUT,
        title="Goles anotados por jugador (ranking)",
        xaxis_tickangle=-30,
        height=420,
        xaxis_tickfont_color="#0d3320",
        yaxis_tickfont_color="#0d3320",
        xaxis_title="Jugador",
        yaxis_title="Goles",
    )
    st.plotly_chart(fig, use_container_width=True)

with col_eq_g:
    goles_por_equipo = (
        df.groupby("equipo")["goles"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    goles_por_equipo.columns = ["Equipo", "Goles totales"]

    n_eq2 = len(goles_por_equipo)
    colores_eq_g = pc.sample_colorscale(
        "Greens",
        [i / max(n_eq2 - 1, 1) for i in range(n_eq2)]
    )

    fig = go.Figure(go.Bar(
        x=goles_por_equipo["Goles totales"],
        y=goles_por_equipo["Equipo"],
        orientation="h",
        marker=dict(
            color=list(reversed(colores_eq_g)),
            line=dict(color="#27ae60", width=0.5),
        ),
        text=goles_por_equipo["Goles totales"],
        textposition="outside",
        textfont=dict(color="#0d3320", size=10),
    ))

    layout = BASE_LAYOUT.copy()
    layout.update({
        "title": "Goles totales del dataset por equipo",
        "height": 420,
        "xaxis_title": "Goles totales",
        "yaxis": dict(
            autorange="reversed",
            gridcolor="#ddeee5",
            zerolinecolor="#b8ddc8",
            color="#1a3a2a",
            tickfont_color="#0d3320",
        ),
    })

    fig.update_layout(**layout)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────

st.markdown("""
<div style="text-align:center; color:#3a6a4a; font-size:0.78rem; padding:0.8rem 0 1.8rem; border-top: 1px solid #c8e8d4;">
    ⚽ Análisis de Jugadores de Fútbol &nbsp;·&nbsp; Estadística I &nbsp;·&nbsp; 2026 &nbsp;·&nbsp; Streamlit · Plotly · Pandas
</div>
""", unsafe_allow_html=True)
