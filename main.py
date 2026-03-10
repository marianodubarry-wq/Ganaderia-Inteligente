import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random

# CONFIGURACIÓN ESTÉTICA
st.set_page_config(page_title="GI - Ganadería Inteligente", layout="wide", page_icon="🐂")

st.markdown("""
    <style>
    .main { background-color: #F8F9F3; }
    h1 { color: #2D5A27; font-family: 'Georgia', serif; font-size: 3rem; margin-bottom: 0px; }
    .sub { color: #5D4037; font-size: 1.1rem; margin-top: 0px; margin-bottom: 2rem; }
    .stMetric { border-left: 5px solid #2D5A27 !important; background-color: white; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("<h1>GANADERÍA INTELIGENTE</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub'>Bienvenido, Productor. Simulación de Máxima Capacidad Activa.</p>", unsafe_allow_html=True)

# --- SIDEBAR (CONFIGURACIÓN) ---
with st.sidebar:
    st.header("⚙️ Configuración")
    moneda = st.radio("Unidad de Medida", ["Pesos (ARS)", "Dólar MEP"], key="unit")
    
    st.divider()
    st.subheader("💰 Precios del Día ($/kg)")
    p_nov = st.number_input("Novillito", value=5211.0)
    p_ter = st.number_input("Ternero", value=5650.0)
    p_vac = st.number_input("Vaca", value=2450.0)
    val_mep = 1433.0 # Cotización Marzo 2026

# --- GENERADOR INTERNO DE DATOS (500 ANIMALES) ---
@st.cache_data # Esto hace que los datos no cambien cada vez que tocas un botón
def generar_rodeo_pesado():
    n = 500
    categorias = {
        "Ternero": {"peso_mu": 185, "sigma": 15, "gmd": 0.750},
        "Novillito": {"peso_mu": 330, "sigma": 25, "gmd": 0.880},
        "Novillo": {"peso_mu": 425, "sigma": 30, "gmd": 0.980}
    }
    rows = []
    for i in range(n):
        cat = random.choice(list(categorias.keys()))
        conf = categorias[cat]
        # Generar peso con distribución normal
        peso = round(np.random.normal(conf["peso_mu"], conf["sigma"]), 1)
        # Inyectar anomalías negativas (animales quedados)
        if i % 35 == 0: peso = peso * 0.7 
        
        rows.append({
            "Caravana": f"320000{random.randint(100000, 999999)}",
            "Peso_Actual": peso,
            "Categoria": cat,
            "Lote": f"Lote_{cat}_Norte"
        })
    return pd.DataFrame(rows)

df = generar_rodeo_pesado()

# --- CUERPO DEL DASHBOARD ---
col_izq, col_der = st.columns([1, 2])

with col_izq:
    st.markdown("### 📊 Mi Rodeo")
    st.metric("Total Hacienda", f"{len(df)} Cabezas")
    
    conteo = df['Categoria'].value_counts()
    for cat, cant in conteo.items():
        st.write(f"**{cat}:** {cant} unidades")
    
    st.divider()
    # Valuación económica
    def valuar(row):
        if row['Categoria'] == "Ternero": return row['Peso_Actual'] * p_ter
        if row['Categoria'] == "Novillito": return row['Peso_Actual'] * p_nov
        return row['Peso_Actual'] * p_vac
    
    df['Valor_Ind'] = df.apply(valuar, axis=1)
    v_total = df['Valor_Ind'].sum()
    
    if moneda == "Dólar MEP":
        st.metric("Capital en Pie", f"USD {(v_total/val_mep):,.0f}")
    else:
        st.metric("Capital en Pie", f"$ {v_total:,.0f}")

with col_der:
    st.markdown("### 🚛 Logística y Oportunidades")
    listos = df[df['Peso_Actual'] >= 380] # Novillos pesados para venta
    
    if len(listos) >= 30:
        st.success(f"🎯 **Jaulas Disponibles:** Tenés {len(listos)} animales listos para venta (+380kg). Completás **{len(listos)//33} jaula(s)**.")
    else:
        st.info(f"Faltan {33 - len(listos)} animales para completar una jaula de gordos.")

    st.divider()
    # ANOMALÍAS (Z-Score)
    st.markdown("### 🚨 Apartar (Anomalías)")
    media_p = df['Peso_Actual'].mean()
    std_p = df['Peso_Actual'].std()
    anomalias = df[df['Peso_Actual'] < (media_p - 2*std_p)]
    
    if not anomalias.empty:
        st.warning(f"Se detectaron {len(anomalias)} animales con bajo rendimiento. Revisar sanidad.")
        st.dataframe(anomalias[['Caravana', 'Peso_Actual', 'Categoria']].head(10), hide_index=True)
    else:
        st.success("Rodeo uniforme. Sin anomalías detectadas.")

# --- GRÁFICO DE CAMPANA DE GAUSS ---
st.divider()
st.markdown("### 📈 Distribución Estadística de Pesos")
fig = px.histogram(df, x="Peso_Actual", color="Categoria", marginal="box", 
                   title="Dispersión de Kilos en el Rodeo Total",
                   color_discrete_sequence=['#2D5A27', '#5D4037', '#A89F91'],
                   labels={'Peso_Actual': 'Peso (kg)', 'count': 'Cantidad de Animales'})
st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠️ Sin datos disponibles. Subí un archivo o revisá el link de Sheets.")


