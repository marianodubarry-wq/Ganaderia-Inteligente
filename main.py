import streamlit as st
import pandas as pd
import numpy as np

# Configuración Estética Minimalista (Campo)
st.set_page_config(page_title="Ganadería Inteligente", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #F5F5F5; }
    .stMetric { background-color: #FFFFFF; padding: 15px; border-radius: 10px; border-left: 5px solid #2D5A27; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    h1, h2, h3 { color: #2D5A27; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (MENÚ LATERAL) ---
st.sidebar.header("🚜 Oficina de Gestión")
moneda = st.sidebar.radio("Unidad de Medida", ["Pesos (ARS)", "Dólar MEP"])
precio_nov = st.sidebar.number_input("Precio Novillito ($/kg)", value=5211.0)
precio_ternero = st.sidebar.number_input("Precio Ternero ($/kg)", value=5600.0)
mep = 1433.0 # Valor marzo 2026

# --- PANTALLA PRINCIPAL ---
st.title("🌾 Ganadería Inteligente")
st.subheader("Tablero de Control - Norte de Santa Fe")

# Indicadores Principales
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("GMD Media Rodeo", "0.785 kg", "2% vs mes ant.")
with col2:
    st.metric("Población Total", "450 Cabezas")
with col3:
    valor_total = 450 * 350 * precio_nov
    if moneda == "Dólar MEP":
        st.metric("Valor del Stock", f"USD {(valor_total/mep):,.0f}")
    else:
        st.metric("Valor del Stock", f"$ {valor_total:,.0f}")

st.divider()

# Sección de Consejos e IA
st.success(f"💡 **Oportunidad Financiera:** Con el precio a ${precio_nov}, tenés 32 novillitos listos para completar una **Jaula Simple**. Relación C/V: {precio_ternero/precio_nov:.2f}")

st.error("⚠️ **Recordatorio de Rejunte:** Apartar caravanas ...892, ...115 (Anomalías detectadas).")

# Sección de Logística (Tabs)
tab1, tab2 = st.tabs(["📋 Inventario", "🚛 Optimización de Jaula"])

with tab1:
    st.write("Aquí se mostrará la lista de animales sincronizada con tu Drive.")
    st.info("Buscador RFID activo en el menú lateral.")

with tab2:
    st.write("🚛 **Transporte sugerido:** Semirremolque Jaula (1 Piso)")
    st.write("Carga actual: 32 Novillitos + 3 Terneros de bajo rendimiento (Relleno).")
