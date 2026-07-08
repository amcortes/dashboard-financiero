import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# 🎨 CONFIGURACIÓN DE ESTILO NATIVO (Más estable)
st.set_page_config(page_title="Dashboard Financiero", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #F0F2F5; }
    /* Aplicamos estilo a los contenedores nativos de Streamlit */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column"] > [data-testid="stVerticalBlock"] {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
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

def obtener_mercado_continuo():
    return {
        "Acciona (ANA.MC)": "ANA.MC", "Acerinox (ACX.MC)": "ACX.MC", "Aena (AENA.MC)": "AENA.MC",
        "Amadeus (AMS.MC)": "AMS.MC", "Banco Santander (SAN.MC)": "SAN.MC",
        "BBVA (BBVA.MC)": "BBVA.MC", "CaixaBank (CABK.MC)": "CABK.MC", "Iberdrola (IBE.MC)": "IBE.MC",
        "Inditex (ITX.MC)": "ITX.MC", "Naturgy (NTGY.MC)": "NTGY.MC", "Repsol (REP.MC)": "REP.MC",
        "Telefónica (TEF.MC)": "TEF.MC"
    }

opciones_tickers = obtener_mercado_continuo()
opciones_tiempo = {"1 Semana": 7, "1 Mes": 30, "3 Meses": 90, "6 Meses": 180, "1 Año": 365, "5 Años": 1825}

st.title("📊 Monitor de Renta Variable y Mercados")

# Sidebar
st.sidebar.header("🕹️ Panel de Control")
seleccion1 = st.sidebar.selectbox("Activo Principal:", list(opciones_tickers.keys()), index=4)
seleccion2 = st.sidebar.selectbox("Activo a Comparar:", list(opciones_tickers.keys()), index=5)
rango_elegido = st.sidebar.selectbox("Rango Temporal:", list(opciones_tiempo.keys()), index=4)
dias_restar = opciones_tiempo[rango_elegido]

ticker1, ticker2 = opciones_tickers[seleccion1], opciones_tickers[seleccion2]

# Carga de datos
with st.spinner("Descargando datos..."):
    fecha_fin = datetime.now()
    fecha_inicio = fecha_fin - timedelta(days=dias_restar + 10)
    
    datos1 = yf.download(ticker1, start=fecha_inicio, end=fecha_fin)
    datos2 = yf.download(ticker2, start=fecha_inicio, end=fecha_fin)
    datos_ibex = yf.download("^IBEX", start=fecha_inicio, end=fecha_fin)
    datos_stoxx = yf.download("^STOXX50E", start=fecha_inicio, end=fecha_fin)

    if not (datos1.empty or datos2.empty):
        
        # 1. CONTENEDOR DE MÉTRICAS
        with st.container():
            st.subheader("📋 Cuadro Comparativo")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric(seleccion1, f"{float(datos1['Close'].iloc[-1]):,.2f} €")
            c2.metric(seleccion2, f"{float(datos2['Close'].iloc[-1]):,.2f} €")
            c3.metric("IBEX 35", f"{float(datos_ibex['Close'].iloc[-1]):,.2f} pts")
            c4.metric("EURO STOXX 50", f"{float(datos_stoxx['Close'].iloc[-1]):,.2f} pts")

        # 2. CONTENEDOR DE GRÁFICO
        with st.container():
            st.subheader(f"📈 Rendimiento Acumulado ({rango_elegido})")
            df_c = pd.concat([datos1['Close'].iloc[:, 0], datos2['Close'].iloc[:, 0]], axis=1).dropna()
            df_c.columns = [seleccion1, seleccion2]
            df_rend = ((df_c.tail(dias_restar) / df_c.tail(dias_restar).iloc[0]) - 1) * 100
            st.line_chart(df_rend)

        # 3. CONTENEDOR DE ESTADÍSTICAS
        with st.container():
            st.subheader("🧮 Laboratorio Estadístico")
            st.dataframe(df_rend.describe().T.style.format("{:,.2f}"), use_container_width=True)
            
    else:
        st.error("Error al descargar los datos. Revisa los activos.")
