import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# 🎨 CONFIGURACIÓN DE ESTILOS CSS PROFESIONALES
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
    div.stButton > button {
        background-color: #1877F2 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# 1. DEFINICIÓN DE FUNCIONES (Primero)
def obtener_mercado_continuo():
    return {
        "Acciona (ANA.MC)": "ANA.MC", "Acerinox (ACX.MC)": "ACX.MC", "Aena (AENA.MC)": "AENA.MC",
        "Amadeus (AMS.MC)": "AMS.MC", "Banco Sabadell (SAB.MC)": "SAB.MC", "Banco Santander (SAN.MC)": "SAN.MC",
        "BBVA (BBVA.MC)": "BBVA.MC", "CaixaBank (CABK.MC)": "CABK.MC", "Iberdrola (IBE.MC)": "IBE.MC",
        "Inditex (ITX.MC)": "ITX.MC", "Naturgy (NTGY.MC)": "NTGY.MC", "Repsol (REP.MC)": "REP.MC",
        "Telefónica (TEF.MC)": "TEF.MC"
    }

# 2. CONFIGURACIÓN E INICIALIZACIÓN
st.set_page_config(page_title="Dashboard Financiero", layout="wide")
opciones_tickers = obtener_mercado_continuo()
opciones_tiempo = {"1 Semana": 7, "1 Mes": 30, "3 Meses": 90, "6 Meses": 180, "1 Año": 365, "5 Años": 1825}

st.title("📊 Monitor de Renta Variable y Mercados")

# 3. BARRA LATERAL
st.sidebar.header("🕹️ Panel de Control")
seleccion1 = st.sidebar.selectbox("Activo Principal:", list(opciones_tickers.keys()), index=5)
seleccion2 = st.sidebar.selectbox("Activo a Comparar:", list(opciones_tickers.keys()), index=3)
rango_elegido = st.sidebar.selectbox("Rango Temporal:", list(opciones_tiempo.keys()), index=4)

ticker1, ticker2 = opciones_tickers[seleccion1], opciones_tickers[seleccion2]
dias_restar = opciones_tiempo[rango_elegido]

# 4. LÓGICA DE DATOS
with st.spinner("Descargando datos..."):
    fecha_fin = datetime.now()
    fecha_inicio = fecha_fin - timedelta(days=dias_restar + 10)
    
    datos1 = yf.download(ticker1, start=fecha_inicio, end=fecha_fin)
    datos2 = yf.download(ticker2, start=fecha_inicio, end=fecha_fin)
    datos_ibex = yf.download("^IBEX", start=fecha_inicio, end=fecha_fin)
    datos_stoxx = yf.download("^STOXX50E", start=fecha_inicio, end=fecha_fin)

    if not datos1.empty and not datos2.empty:
        # --- TARJETA DE MÉTRICAS ---
        st.markdown('<div class="css-card">', unsafe_allow_html=True)
        st.subheader("📋 Cuadro Comparativo")
        # Aquí iría tu lógica de cálculo de métricas previa...
        st.info("Panel de métricas activo.") 
        st.markdown('</div>', unsafe_allow_html=True)

        # --- TARJETA DE GRÁFICO ---
        st.markdown('<div class="css-card">', unsafe_allow_html=True)
        st.subheader(f"📈 Rendimiento Acumulado ({rango_elegido})")
        # Cálculo simple para el ejemplo
        df_plot = pd.concat([datos1['Close'], datos2['Close']], axis=1).dropna()
        st.line_chart(df_plot)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("Error al obtener datos.")
