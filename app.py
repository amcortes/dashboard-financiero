# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 11:46:59 2026

@author: anton
"""

import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np

def obtener_mercado_continuo():
    # Lista interna con los principales activos del Mercado Continuo español
    return {
        "Acciona (ANA.MC)": "ANA.MC",
        "Acerinox (ACX.MC)": "ACX.MC",
        "Aena (AENA.MC)": "AENA.MC",
        "Amadeus (AMS.MC)": "AMS.MC",
        "Applus (APPS.MC)": "APPS.MC",
        "Arima (ARM.MC)": "ARM.MC",
        "Banco Sabadell (SAB.MC)": "SAB.MC",
        "Banco Santander (SAN.MC)": "SAN.MC",
        "Bankinter (BKT.MC)": "BKT.MC",
        "BBVA (BBVA.MC)": "BBVA.MC",
        "CaixaBank (CABK.MC)": "CABK.MC",
        "Cellnex (CLNX.MC)": "CLNX.MC",
        "Enagás (ENG.MC)": "ENG.MC",
        "Endesa (ELE.MC)": "ELE.MC",
        "Ercros (ECR.MC)": "ECR.MC",
        "Faes Farma (FAE.MC)": "FAE.MC",
        "Ferrovial (FER.MC)": "FER.MC",
        "Fluidra (FDR.MC)": "FDR.MC",
        "Grifols (GRF.MC)": "GRF.MC",
        "Iberdrola (IBE.MC)": "IBE.MC",
        "Inditex (ITX.MC)": "ITX.MC",
        "Indra (IDR.MC)": "IDR.MC",
        "Inmobiliaria Colonial (COL.MC)": "COL.MC",
        "Logista (LOG.MC)": "LOG.MC",
        "Mapfre (MAP.MC)": "MAP.MC",
        "Meliá Hotels (MEL.MC)": "MEL.MC",
        "Naturgy (NTGY.MC)": "NTGY.MC",
        "PharmaMar (PHM.MC)": "PHM.MC",
        "Repsol (REP.MC)": "REP.MC",
        "Sacyr (SCYR.MC)": "SCYR.MC",
        "Solaria (SLR.MC)": "SLR.MC",
        "Telefónica (TEF.MC)": "TEF.MC",
        "Unicaja Banco (UNI.MC)": "UNI.MC"
    }

# Asignamos la lista al menú lateral
opciones_tickers = obtener_mercado_continuo()

# 📊 Configuración de la página web
st.set_page_config(page_title="Dashboard Financiero", layout="wide")

# 🏛️ Banner de título
st.title("📊 Monitor de Renta Variable y Mercados")
st.markdown("---")

# 🟢 Panel de Control (Barra lateral para los alumnos)
st.sidebar.header("🕹️ Panel de Control")

seleccion = st.sidebar.selectbox("Selecciona un Activo para analizar:", list(opciones_tickers.keys()))
ticker = opciones_tickers[seleccion]

# Botón para activar la carga
if st.sidebar.button("🔄 Actualizar Mercado"):
    
    with st.spinner("Descargando datos en vivo..."):
        # 📅 Calcular fechas (últimos 12 meses)
        fecha_fin = datetime.now()
        fecha_inicio = fecha_fin - timedelta(days=365)
        
        # 📥 Descarga de datos mediante yfinance
        datos = yf.download(ticker, start=fecha_inicio, end=fecha_fin)
        
        if not datos.empty:
            # 📈 Extracción de precios y cálculos financieros
            # yfinance devuelve un DataFrame; extraemos los valores de cierre ajustado
            precios_cierre = datos[('Close', ticker)]
            precio_actual = float(precios_cierre.iloc[-1])
            precio_anterior = float(precios_cierre.iloc[-2])
            
            # Rendimiento diario
            var_diaria = (precio_actual - precio_anterior) / precio_anterior
            
            # Máximos y mínimos de 52 semanas
            max_52 = float(precios_cierre.max())
            min_52 = float(precios_cierre.min())
            
            # Volatilidad histórica anualizada (Rendimientos logarítmicos)
            rendimientos_log = np.log(precios_cierre / precios_cierre.shift(1)).dropna()
            vol_anual = float(rendimientos_log.std() * np.sqrt(252))
            
            # 🔵 Bloque de Tarjetas Informativas
            col1, col2, col3, col4 = st.columns(4)
            
            col1.metric(
                label="💰 Precio Actual", 
                value=f"${precio_actual:,.2f}"
            )
            
            col2.metric(
                label="📊 Var. Diaria (%)", 
                value=f"{var_diaria:+.2f}%",
                delta=f"{var_diaria:+.2f}%"
            )
            
            col3.metric(
                label="📈 Máx / Mín (52 sem)", 
                value=f"${max_52:,.0f} / ${min_52:,.0f}"
            )
            
            col4.metric(
                label="📉 Volatilidad Anual", 
                value=f"{vol_anual:.2f}%"
            )
            
            st.markdown("---")
            
            # 🟡 Bloque de Gráfico Interactivo
            st.subheader(f"📈 Evolución Histórica de {seleccion}")
            st.line_chart(precios_cierre.rename("Precio de Cierre"))
            
        else:
            st.error("No se pudieron obtener datos para este ticker. Revisa la conexión.")
else:
    st.info("👋 ¡Bienvenido! Selecciona un activo en el panel de la izquierda y haz clic en 'Actualizar Mercado' para comenzar el análisis con tus alumnos.")
