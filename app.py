import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# 🎨 CSS PROFESIONAL
st.markdown("""
<style>
    .stApp { background-color: #F0F2F5; }
    .css-card {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 25px;
        border: 1px solid #E1E4E8;
    }
    h1, h2, h3 { color: #1C1E21 !important; }
    /* Ajuste para que las tablas se vean integradas */
    [data-testid="stDataFrame"] { border: none !important; }
    div.stButton > button {
        background-color: #1877F2 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# ... (mantén tu función obtener_mercado_continuo aquí) ...

st.set_page_config(page_title="Dashboard Financiero", layout="wide")

st.title("📊 Monitor de Renta Variable y Mercados")

# --- PANEL DE CONTROL (sidebar) ---
st.sidebar.header("🕹️ Panel de Control")
seleccion1 = st.sidebar.selectbox("Activo Principal:", list(opciones_tickers.keys()), index=7)
seleccion2 = st.sidebar.selectbox("Activo a Comparar:", list(opciones_tickers.keys()), index=9)
rango_elegido = st.sidebar.selectbox("Rango Temporal:", list(opciones_tiempo.keys()), index=4)
dias_restar = opciones_tiempo[rango_elegido]
ticker1, ticker2 = opciones_tickers[seleccion1], opciones_tickers[seleccion2]

# --- LÓGICA DE DATOS ---
with st.spinner("Descargando datos en vivo..."):
    fecha_fin = datetime.now()
    fecha_inicio = fecha_fin - timedelta(days=max(dias_restar, 10))
    datos1, datos2 = yf.download(ticker1, fecha_inicio, fecha_fin), yf.download(ticker2, fecha_inicio, fecha_fin)
    datos_ibex, datos_stoxx = yf.download("^IBEX", fecha_inicio, fecha_fin), yf.download("^STOXX50E", fecha_inicio, fecha_fin)

    if not (datos1.empty or datos2.empty or datos_ibex.empty or datos_stoxx.empty):
        
        # --- TARJETA 1: MÉTRICAS ---
        st.markdown('<div class="css-card">', unsafe_allow_html=True)
        st.subheader("📋 Cuadro Comparativo de Indicadores")
        # (Aquí calculas tus p_act1, v_dir1, vol1... como ya tenías)
        # Usa st.columns dentro del div para mantener el orden
        c1, c2, c3, c4 = st.columns(4)
        c1.metric(seleccion1, f"{p_act1:,.2f} €", f"{v_dir1*100:+.2f}%")
        c2.metric(seleccion2, f"{p_act2:,.2f} €", f"{v_dir2*100:+.2f}%")
        c3.metric("IBEX 35", f"{p_act_ib:,.2f} pts", f"{v_dir_ib*100:+.2f}%")
        c4.metric("EURO STOXX 50", f"{p_act_st:,.2f} pts", f"{v_dir_st*100:+.2f}%")
        st.markdown('</div>', unsafe_allow_html=True)

        # --- TARJETA 2: GRÁFICO ---
        st.markdown('<div class="css-card">', unsafe_allow_html=True)
        st.subheader(f"📈 Análisis de Rendimiento Acumulado")
        # (Realiza tus cálculos de df_rendimiento aquí)
        st.line_chart(df_rendimiento)
        st.markdown('</div>', unsafe_allow_html=True)

        # --- TARJETA 3: ESTADÍSTICAS ---
        st.markdown('<div class="css-card">', unsafe_allow_html=True)
        st.subheader("🧮 Laboratorio Estadístico")
        df_desc = df_rendimiento.describe().T
        st.dataframe(df_desc.style.format("{:,.2f}"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.error("Error al cargar datos.")
