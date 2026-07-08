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

# Selección de los dos activos individuales
seleccion1 = st.sidebar.selectbox("Selecciona el Activo Principal:", list(opciones_tickers.keys()), index=7) # Santander
ticker1 = opciones_tickers[seleccion1]

seleccion2 = st.sidebar.selectbox("Selecciona el Activo a Comparar:", list(opciones_tickers.keys()), index=9) # BBVA
ticker2 = opciones_tickers[seleccion2]

# 🔄 Carga automática de datos
with st.spinner("Descargando datos en vivo..."):
    fecha_fin = datetime.now()
    fecha_inicio = fecha_fin - timedelta(days=365)
    
    # Descarga de los 4 elementos necesarios
    datos1 = yf.download(ticker1, start=fecha_inicio, end=fecha_fin)
    datos2 = yf.download(ticker2, start=fecha_inicio, end=fecha_fin)
    datos_ibex = yf.download("^IBEX", start=fecha_inicio, end=fecha_fin)
    datos_stoxx = yf.download("^STOXX50E", start=fecha_inicio, end=fecha_fin)
    
    if not (datos1.empty or datos2.empty or datos_ibex.empty or datos_stoxx.empty):
        
        # Función auxiliar para extraer métricas clave de un DataFrame de yfinance
        def calcular_metricas(df, ticker_sym):
            cierre = df[('Close', ticker_sym)] if ('Close', ticker_sym) in df.columns else df['Close']
            if isinstance(cierre, pd.DataFrame):
                cierre = cierre.iloc[:, 0]
            
            act = float(cierre.iloc[-1])
            ant = float(cierre.iloc[-2])
            var = (act - ant) / ant
            mx = float(cierre.max())
            mn = float(cierre.min())
            
            rend_log = np.log(cierre / cierre.shift(1)).dropna()
            vol = float(rend_log.std() * np.sqrt(252)) * 100
            return act, var, mx, mn, vol, cierre

        # Calcular métricas para cada uno
        p_act1, v_dir1, mx1, mn1, vol1, c1 = calcular_metricas(datos1, ticker1)
        p_act2, v_dir2, mx2, mn2, vol2, c2 = calcular_metricas(datos2, ticker2)
        p_act_ib, v_dir_ib, mx_ib, mn_ib, vol_ib, c_ib = calcular_metricas(datos_ibex, "^IBEX")
        p_act_st, v_dir_st, mx_st, mn_st, vol_st, c_st = calcular_metricas(datos_stoxx, "^STOXX50E")

        # 🔵 BLOQUE DE TARJETAS INFORMATIVAS EN COLUMNAS COMPARATIVAS
        st.subheader("📋 Cuadro Comparativo de Indicadores Actuales")
        
        # Fila de Nombres de Columnas
        col_lbl, col_a1, col_a2, col_ib, col_st = st.columns([1.5, 2, 2, 2, 2])
        col_a1.markdown(f"**🟢 {seleccion1}**")
        col_a2.markdown(f"**🔵 {seleccion2}**")
        col_ib.markdown("**🏛️ IBEX 35**")
        col_st.markdown("**🇪🇺 EURO STOXX 50**")
        
        st.markdown("---")
        
        # Fila 1: Precio Actual
        c_lbl, c_a1, c_a2, c_ib, c_st = st.columns([1.5, 2, 2, 2, 2])
        c_lbl.markdown("**💰 Precio Actual**")
        c_a1.metric("", f"{p_act1:,.2f} €")
        c_a2.metric("", f"{p_act2:,.2f} €")
        c_ib.metric("", f"{p_act_ib:,.2f} pts")
        c_st.metric("", f"{p_act_st:,.2f} pts")
        
        # Fila 2: Variación Diaria
        v_lbl, v_a1, v_a2, v_ib, v_st = st.columns([1.5, 2, 2, 2, 2])
        v_lbl.markdown("**📊 Var. Diaria (%)**")
        v_a1.metric("", f"{v_dir1 * 100:+.2f}%", delta=f"{v_dir1 * 100:+.2f}%")
        v_a2.metric("", f"{v_dir2 * 100:+.2f}%", delta=f"{v_dir2 * 100:+.2f}%")
        v_ib.metric("", f"{v_dir_ib * 100:+.2f}%", delta=f"{v_dir_ib * 100:+.2f}%")
        v_st.metric("", f"{v_dir_st * 100:+.2f}%", delta=f"{v_dir_st * 100:+.2f}%")
        
        # Fila 3: Volatilidad Anual
        vo_lbl, vo_a1, vo_a2, vo_ib, vo_st = st.columns([1.5, 2, 2, 2, 2])
        vo_lbl.markdown("**📉 Volatilidad Anual**")
        vo_a1.metric("", f"{vol1:.2f}%")
        vo_a2.metric("", f"{vol2:.2f}%")
        vo_ib.metric("", f"{vol_ib:.2f}%")
        vo_st.metric("", f"{vol_st:.2f}%")
        
        st.markdown("---")
        
        # 🧮 CÁLCULO DE COMPARACIÓN CUÁDRUPLE (Rendimiento Acumulado %)
        df_comparativo = pd.DataFrame({
            seleccion1: c1,
            seleccion2: c2,
            "IBEX 35": c_ib,
            "EURO STOXX 50": c_st
        }).dropna()
        
        # Base 0% para todas las series financieras
        df_rendimiento = ((df_comparativo / df_comparativo.iloc[0]) - 1) * 100
        
        # 🟡 Bloque de Gráfico Interactivo Cuádruple
        st.subheader("📈 Análisis de Rendimiento Acumulado")
        st.markdown("*Evolución en porcentaje (%) partiendo desde la misma base inicial para analizar el comportamiento relativo.*")
        st.line_chart(df_rendimiento)
        
    else:
        st.error("Error al descargar los datos de mercado. Revisa la conexión o los símbolos de los activos.")
