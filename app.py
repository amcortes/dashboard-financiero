# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 11:46:59 2026

@author: anton
"""

import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

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

# 🔄 Carga automática e instantánea al cambiar el desplegable
with st.spinner("Descargando datos en vivo..."):
    # 📅 Calcular fechas (últimos 12 meses)
    fecha_fin = datetime.now()
    fecha_inicio = fecha_fin - timedelta(days=365)
    
    # 📥 Descarga de datos mediante yfinance (Activo + IBEX 35)
    datos = yf.download(ticker, start=fecha_inicio, end=fecha_fin)
    datos_ibex = yf.download("^IBEX", start=fecha_inicio, end=fecha_fin)
    
    if not datos.empty and not datos_ibex.empty:
        # 📈 Extracción de precios y cálculos financieros del activo principal
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
        vol_anual = float(rendimientos_log.std() * np.sqrt(252)) * 100
        
        # 🔵 Bloque de Tarjetas Informativas
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric(
            label="💰 Precio Actual", 
            value=f"{precio_actual:,.2f} €"
        )
        
        col2.metric(
            label="📊 Var. Diaria (%)", 
            value=f"{var_diaria * 100:+.2f}%",
            delta=f"{var_diaria * 100:+.2f}%"
        )
        
        col3.metric(
            label="📈 Máx / Mín (52 sem)", 
            value=f"{max_52:,.2f} € / {min_52:,.2f} €"
        )
        
        col4.metric(
            label="📉 Volatilidad Anual", 
            value=f"{vol_anual:.2f}%"
        )
        
        st.markdown("---")
        
        # 🧮 CÁLCULO DE COMPARACIÓN (Rendimiento Acumulado %)
        # Extraemos cierres del IBEX
        precios_ibex = datos_ibex['Close']
        if isinstance(precios_ibex, pd.DataFrame):
            precios_ibex = precios_ibex.iloc[:, 0]
            
        # Alineamos fechas comunes para evitar errores en el gráfico
        df_comparativo = pd.DataFrame({
            seleccion: precios_cierre,
            "IBEX 35": precios_ibex
        }).dropna()
        
        # Calculamos el rendimiento desde el primer día de la serie (base 0%)
        df_rendimiento = ((df_comparativo / df_comparativo.iloc[0]) - 1) * 100
        
        # 🟡 Bloque de Gráfico Interactivo de Comparación
        st.subheader(f"📈 Rendimiento Relativo: {seleccion} vs IBEX 35")
        st.markdown("*Muestra la evolución en porcentaje (%) partiendo desde el mismo punto inicial.*")
        st.line_chart(df_rendimiento)
        
    else:
        st.error("No se pudieron obtener datos para este ticker o para el IBEX 35. Revisa la conexión.")
