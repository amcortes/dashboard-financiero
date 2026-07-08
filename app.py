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

st.markdown("""
<style>
    /* Fondo global gris muy claro */
    .stApp {
        background-color: #F0F2F5;
    }
    
    /* Estilo para las tarjetas de contenido */
    .css-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }

    /* Ajuste de colores de texto */
    h1, h2, h3 { color: #1C1E21 !important; }
    
    /* Estilo del botón de la barra lateral */
    div.stButton > button {
        background-color: #1877F2 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

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

st.sidebar.markdown("---")

# 📅 Configuración de Rango Temporal
opciones_tiempo = {
    "1 Semana": 7,
    "1 Mes": 30,
    "3 Meses": 90,
    "6 Meses": 180,
    "1 Año": 365,
    "5 Años": 5 * 365
}
rango_elegido = st.sidebar.selectbox("Selecciona el Rango Temporal:", list(opciones_tiempo.keys()), index=4) # Por defecto 1 Año
dias_restar = opciones_tiempo[rango_elegido]

# 🔄 Carga automática de datos
with st.spinner("Descargando datos en vivo..."):
    fecha_fin = datetime.now()
    
    # Margen de seguridad para cubrir fines de semana y festivos
    dias_descarga = max(dias_restar, 10)
    fecha_inicio = fecha_fin - timedelta(days=dias_descarga)
    
    # Descarga de los 4 elementos necesarios
    datos1 = yf.download(ticker1, start=fecha_inicio, end=fecha_fin)
    datos2 = yf.download(ticker2, start=fecha_inicio, end=fecha_fin)
    datos_ibex = yf.download("^IBEX", start=fecha_inicio, end=fecha_fin)
    datos_stoxx = yf.download("^STOXX50E", start=fecha_inicio, end=fecha_fin)
    
    if not (datos1.empty or datos2.empty or datos_ibex.empty or datos_stoxx.empty):
        
        # Función auxiliar para extraer métricas clave de un DataFrame de yfinance
        def calcular_metricas(df, ticker_sym, rango):
            cierre = df[('Close', ticker_sym)] if ('Close', ticker_sym) in df.columns else df['Close']
            if isinstance(cierre, pd.DataFrame):
                cierre = cierre.iloc[:, 0]
            
            act = float(cierre.iloc[-1])
            ant = float(cierre.iloc[-2])
            var = (act - ant) / ant
            
            # Saltamos métricas avanzadas si el rango es de 1 Semana
            if rango in ["1 Semana"]:
                vol_str = "N/A"
            else:
                rend_log = np.log(cierre / cierre.shift(1)).dropna()
                if len(rend_log) > 2:
                    vol = float(rend_log.std() * np.sqrt(252)) * 100
                    vol_str = f"{vol:.2f}%"
                else:
                    vol_str = "N/A"
                    
            return act, var, vol_str, cierre

        # Calcular métricas para cada uno
        p_act1, v_dir1, vol1, c1 = calcular_metricas(datos1, ticker1, rango_elegido)
        p_act2, v_dir2, vol2, c2 = calcular_metricas(datos2, ticker2, rango_elegido)
        p_act_ib, v_dir_ib, vol_ib, c_ib = calcular_metricas(datos_ibex, "^IBEX", rango_elegido)
        p_act_st, v_dir_st, vol_st, c_st = calcular_metricas(datos_stoxx, "^STOXX50E", rango_elegido)

        # 🔵 BLOQUE DE TARJETAS INFORMATIVAS EN COLUMNAS COMPARATIVAS
        st.subheader(f"📋 Cuadro Comparativo de Indicadores ({rango_elegido})")
        
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
        vo_lbl.markdown(f"**📉 Volatilidad Anual**")
        vo_a1.metric("", vol1)
        vo_a2.metric("", vol2)
        vo_ib.metric("", vol_ib)
        vo_st.metric("", vol_st)
        
        st.markdown("---")
        
        # 🧮 CÁLCULO DE COMPARACIÓN CUÁDRUPLE (Rendimiento Acumulado %)
        s1 = datos1['Close'].iloc[:, 0] if isinstance(datos1['Close'], pd.DataFrame) else datos1['Close']
        s2 = datos2['Close'].iloc[:, 0] if isinstance(datos2['Close'], pd.DataFrame) else datos2['Close']
        s_ib = datos_ibex['Close'].iloc[:, 0] if isinstance(datos_ibex['Close'], pd.DataFrame) else datos_ibex['Close']
        s_st = datos_stoxx['Close'].iloc[:, 0] if isinstance(datos_stoxx['Close'], pd.DataFrame) else datos_stoxx['Close']
            
        # 🤝 Unimos las 4 series
        df_comparativo = pd.concat([s1, s2, s_ib, s_st], axis=1)
        df_comparativo.columns = [seleccion1, seleccion2, "IBEX 35", "EURO STOXX 50"]
        df_comparativo = df_comparativo.dropna()
        
        # Filtramos el dataframe para usar estrictamente el rango elegido
        df_comparativo = df_comparativo.tail(dias_restar)
        
        # Calculamos el rendimiento acumulado partiendo de base 0%
        df_rendimiento = ((df_comparativo / df_comparativo.iloc[0]) - 1) * 100
        
        # 🟡 Bloque de Gráfico Interactivo Cuádruple
        st.subheader(f"📈 Análisis de Rendimiento Acumulado ({rango_elegido})")
        st.markdown(f"*Evolución en porcentaje (%) partiendo desde la misma base inicial para analizar el comportamiento relativo.*")
        st.markdown('<div class="css-card">', unsafe_allow_html=True)
        st.line_chart(df_rendimiento)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 📊 NUEVO: TABLA DE ESTADÍSTICOS DESCRIPTIVOS
        st.markdown('<div class="css-card">', unsafe_allow_html=True)
        st.subheader(f"🧮 Laboratorio Estadístico de Rendimientos ({rango_elegido})")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("*Análisis detallado de la distribución de los rendimientos acumulados (%) que se muestran en el gráfico superior.*")
        
        # Generar tabla descriptiva con Pandas y transponerla para mejor lectura visual en pantalla
        df_descriptivo = df_rendimiento.describe().T
        
        # Traducir los nombres técnicos de Pandas a términos legibles y financieros
        df_descriptivo = df_descriptivo.rename(columns={
            "count": "Días Analizados",
            "mean": "Rendimiento Medio (%)",
            "std": "Desviación Estándar (%)",
            "min": "Rendimiento Mínimo (%)",
            "25%": "Percentil 25 (%)",
            "50%": "Mediana (%)",
            "75%": "Percentil 75 (%)",
            "max": "Rendimiento Máximo (%)"
        })
        
        # Dar formato de dos decimales a los datos numéricos de la tabla
        st.dataframe(df_descriptivo.style.format("{:,.2f}"))
        
    else:
        st.error("Error al descargar los datos de mercado. Revisa la conexión o los símbolos de los activos.")
