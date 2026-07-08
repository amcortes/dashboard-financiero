import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# 🎨 CSS PROFESIONAL
st.markdown("""
<style>
    .stApp { background-color: #F0F2F5; }
    .card {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 25px;
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
        "Amadeus (AMS.MC)": "AMS.MC", "Applus (APPS.MC)": "APPS.MC", "Arima (ARM.MC)": "ARM.MC",
        "Banco Sabadell (SAB.MC)": "SAB.MC", "Banco Santander (SAN.MC)": "SAN.MC", "Bankinter (BKT.MC)": "BKT.MC",
        "BBVA (BBVA.MC)": "BBVA.MC", "CaixaBank (CABK.MC)": "CABK.MC", "Cellnex (CLNX.MC)": "CLNX.MC",
        "Enagás (ENG.MC)": "ENG.MC", "Endesa (ELE.MC)": "ELE.MC", "Ercros (ECR.MC)": "ECR.MC",
        "Faes Farma (FAE.MC)": "FAE.MC", "Ferrovial (FER.MC)": "FER.MC", "Fluidra (FDR.MC)": "FDR.MC",
        "Grifols (GRF.MC)": "GRF.MC", "Iberdrola (IBE.MC)": "IBE.MC", "Inditex (ITX.MC)": "ITX.MC",
        "Indra (IDR.MC)": "IDR.MC", "Inmobiliaria Colonial (COL.MC)": "COL.MC", "Logista (LOG.MC)": "LOG.MC",
        "Mapfre (MAP.MC)": "MAP.MC", "Meliá Hotels (MEL.MC)": "MEL.MC", "Naturgy (NTGY.MC)": "NTGY.MC",
        "PharmaMar (PHM.MC)": "PHM.MC", "Repsol (REP.MC)": "REP.MC", "Sacyr (SCYR.MC)": "SCYR.MC",
        "Solaria (SLR.MC)": "SLR.MC", "Telefónica (TEF.MC)": "TEF.MC", "Unicaja Banco (UNI.MC)": "UNI.MC"
    }

opciones_tickers = obtener_mercado_continuo()
st.set_page_config(page_title="Dashboard Financiero", layout="wide")
st.title("📊 Monitor de Renta Variable y Mercados")

st.sidebar.header("🕹️ Panel de Control")
seleccion1 = st.sidebar.selectbox("Selecciona el Activo Principal:", list(opciones_tickers.keys()), index=7)
ticker1 = opciones_tickers[seleccion1]
seleccion2 = st.sidebar.selectbox("Selecciona el Activo a Comparar:", list(opciones_tickers.keys()), index=9)
ticker2 = opciones_tickers[seleccion2]

opciones_tiempo = {"1 Semana": 7, "1 Mes": 30, "3 Meses": 90, "6 Meses": 180, "1 Año": 365, "5 Años": 1825}
rango_elegido = st.sidebar.selectbox("Selecciona el Rango Temporal:", list(opciones_tiempo.keys()), index=4)
dias_restar = opciones_tiempo[rango_elegido]

with st.spinner("Descargando datos..."):
    fecha_fin = datetime.now()
    datos1 = yf.download(ticker1, start=fecha_fin - timedelta(days=dias_restar + 10), end=fecha_fin)
    datos2 = yf.download(ticker2, start=fecha_fin - timedelta(days=dias_restar + 10), end=fecha_fin)
    datos_ibex = yf.download("^IBEX", start=fecha_fin - timedelta(days=dias_restar + 10), end=fecha_fin)
    datos_stoxx = yf.download("^STOXX50E", start=fecha_fin - timedelta(days=dias_restar + 10), end=fecha_fin)

    if not (datos1.empty or datos2.empty or datos_ibex.empty or datos_stoxx.empty):
        def calcular_metricas(df, ticker_sym):
            cierre = df[('Close', ticker_sym)] if ('Close', ticker_sym) in df.columns else df['Close']
            cierre = cierre.iloc[:, 0] if isinstance(cierre, pd.DataFrame) else cierre
            act = float(cierre.iloc[-1])
            var = (act - float(cierre.iloc[-2])) / float(cierre.iloc[-2])
            return act, var

        p1, v1 = calcular_metricas(datos1, ticker1)
        p2, v2 = calcular_metricas(datos2, ticker2)
        pib, vib = calcular_metricas(datos_ibex, "^IBEX")
        pst, vst = calcular_metricas(datos_stoxx, "^STOXX50E")

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader(f"📋 Cuadro Comparativo ({rango_elegido})")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric(seleccion1, f"{p1:,.2f} €", f"{v1*100:+.2f}%")
        c2.metric(seleccion2, f"{p2:,.2f} €", f"{v2*100:+.2f}%")
        c3.metric("IBEX 35", f"{pib:,.2f} pts", f"{vib*100:+.2f}%")
        c4.metric("EURO STOXX 50", f"{pst:,.2f} pts", f"{vst*100:+.2f}%")
        st.markdown('</div>', unsafe_allow_html=True)

        df_c = pd.concat([datos1['Close'].iloc[:, 0], datos2['Close'].iloc[:, 0], 
                          datos_ibex['Close'].iloc[:, 0], datos_stoxx['Close'].iloc[:, 0]], axis=1).dropna()
        df_c.columns = [seleccion1, seleccion2, "IBEX 35", "EURO STOXX 50"]
        df_rend = ((df_c.tail(dias_restar) / df_c.tail(dias_restar).iloc[0]) - 1) * 100

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader(f"📈 Rendimiento Acumulado")
        st.line_chart(df_rend)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🧮 Laboratorio Estadístico")
        st.dataframe(df_rend.describe().T.style.format("{:,.2f}"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("Error al cargar datos.")
