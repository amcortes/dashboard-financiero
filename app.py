import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# 🎨 CSS PROFESIONAL
st.markdown("""
<style>
    .stApp { background-color: #F0F2F5; }
    /* Clase para los contenedores */
    .card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    h1, h2, h3 { color: #1C1E21 !important; }
</style>
""", unsafe_allow_html=True)

# ... (mantén aquí tu función obtener_mercado_continuo igual) ...

st.set_page_config(page_title="Dashboard Financiero", layout="wide")
st.title("📊 Monitor de Renta Variable y Mercados")

# --- LÓGICA DE DATOS (Igual que tenías) ---
# ... (asegúrate de mantener todo el bloque del with st.spinner) ...

    if not (datos1.empty or datos2.empty or datos_ibex.empty or datos_stoxx.empty):
        
        # 1. TARJETA DE MÉTRICAS
        # Usamos un contenedor para envolver las columnas sin romperlas
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader(f"📋 Cuadro Comparativo de Indicadores ({rango_elegido})")
            
            # Tus columnas dentro de la card
            col_lbl, col_a1, col_a2, col_ib, col_st = st.columns([1.5, 2, 2, 2, 2])
            # ... (Tus .markdown y .metric de siempre) ...
            st.markdown('</div>', unsafe_allow_html=True)

        # 2. TARJETA DE GRÁFICO
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader(f"📈 Análisis de Rendimiento Acumulado")
            st.line_chart(df_rendimiento)
            st.markdown('</div>', unsafe_allow_html=True)

        # 3. TARJETA DE TABLA
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader(f"🧮 Laboratorio Estadístico")
            # Usamos use_container_width para que ocupe el ancho de la tarjeta
            st.dataframe(df_descriptivo.style.format("{:,.2f}"), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
