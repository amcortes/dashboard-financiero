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

@st.cache_data(ttl=86400)  # Guarda la lista en memoria durante 24h para que la web cargue ultra rápido
def obtener_mercado_continuo():
    try:
        # Lee las tablas de la página de Wikipedia del Mercado Continuo
        url = "https://es.wikipedia.org/wiki/Mercado_Continuo_Espa%C3%B1ol"
        tablas = pd.read_html(url)
        
        # La tabla principal suele ser la primera o segunda (índice 0 o 1)
        # Buscamos la tabla que contenga la columna 'Ticker' o 'Empresa'
        df = None
        for t in tablas:
            if 'Ticker' in t.columns:
                df = t
                break
        
        if df is not None:
            # Creamos el diccionario dinámico: "Nombre de Empresa (TICKER.MC)": "TICKER.MC"
            diccionario_activos = {}
            for _, fila in df.iterrows():
                ticker_raw = str(fila['Ticker']).strip()
                empresa = str(fila['Empresa']).strip()
                
                # Nos aseguramos de que el ticker termine en .MC (formato Yahoo Finance)
                if not ticker_raw.endswith('.MC'):
                    ticker_yf = f"{ticker_raw}.MC"
                else:
                    ticker_yf = ticker_raw
                    
                nombre_menu = f"{empresa} ({ticker_yf})"
                diccionario_activos[nombre_menu] = ticker_yf
                
            return diccionario_activos
    except Exception as e:
        print(f"Error al conectar con Wikipedia: {e}")
        # Si Wikipedia falla por algún motivo, devolvemos una lista de emergencia para que la web no se rompa
        return {"Banco Santander (SAN.MC)": "SAN.MC", "BBVA (BBVA.MC)": "BBVA.MC", "Telefónica (TEF.MC)": "TEF.MC"}

# Llamamos a la función para cargar los activos dinámicos
opciones_tickers = obtener_mercado_continuo()
st.write(opciones_tickers)



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
