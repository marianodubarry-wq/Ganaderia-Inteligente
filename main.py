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
    .stMetric { border-left: 5px solid #2D5A27 !important; background-color: white; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("<h1>GANADERÍA INTELIGENTE</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub'>Bienvenido, Productor. Gestión Bioeconómica de Precisión.</p>", unsafe_allow_html=True)

# --- SIDEBAR (CONFIGURACIÓN) ---
with st.sidebar:
    st.header("⚙️ Configuración")
    moneda = st.radio("Unidad de Medida", ["Pesos (ARS)", "Dólar MEP"], key="unit")
    st.divider()
    st.subheader("💰 Precios de Mercado ($/kg)")
    p_nov = st.number_input("Novillito", value=5211.0)
    p_ter = st.number_input("Ternero", value=5650.0)
    p_vac = st.number_input("Vaca", value=2450.0)
    val_mep = 1433.0

# --- GENERADOR INTERNO DE DATOS (500 ANIMALES) ---
@st.cache_data
def generar_rodeo():
    n = 500
    cats = {
        "Ternero": {"mu": 185, "sd": 15, "p": p_ter},
        "Novillito": {"mu": 330, "sd": 25, "p": p_nov},
        "Novillo": {"mu": 425, "sd": 30, "p": p_nov}
    }
    rows = []
    for i in range(n):
        c = random.choice(list(cats.keys()))
        peso = round(np.random.normal(cats[c]["mu"], cats[c]["sd"]), 1)
        if i % 35 == 0: peso *= 0.7 # Anomalía
        rows.append({"Caravana": f"320000{random.randint(100000,999999)}", "Peso": peso, "Categoria": c})
    return pd.DataFrame(rows)

df = generar_rodeo()

# Valuación
def calcular_valor(row):
    if row['Categoria'] == "Ternero": return row['Peso'] * p_ter
    if row['Categoria'] == "Novillito": return row['Peso'] * p_nov
    return row['Peso'] * p_nov # Para Novillo usamos precio novillito o similar

df['Valor_ARS'] = df.apply(calcular_valor, axis=1)
valor_total_ars = df['Valor_ARS'].sum()

# --- CUERPO PRINCIPAL ---
col_izq, col_der = st.columns([1, 2])

with col_izq:
    st.markdown("### 📊 Mi Rodeo")
    st.metric("Total Hacienda", f"{len(df)} Cabezas")
    
    for cat, cant in df['Categoria'].value_counts().items():
        st.write(f"**{cat}:** {cant}")
    
    st.divider()
    if moneda == "Dólar MEP":
        st.metric("Capital en Pie", f"USD {(valor_total_ars/val_mep):,.0f}")
    else:
        st.metric("Capital en Pie", f"$ {valor_total_ars:,.0f}")

with col_der:
    st.markdown("### 🚛 Logística y Alertas")
    listos = df[df['Peso'] >= 380]
    if len(listos) >= 30:
        st.success(f"🎯 **Jaulas:** {len(listos)} animales listos. Completás **{len(listos)//33} jaula(s)**.")
    else:
        st.info(f"Faltan {33 - len(listos)} animales para una jaula completa.")

    st.divider()
    media = df['Peso'].mean()
    std = df['Peso'].std()
    anomalias = df[df['Peso'] < (media - 2*std)]
    if not anomalias.empty:
        st.warning(f"🚨 {len(anomalias)} Anomalías de peso detectadas.")
        st.dataframe(anomalias[['Caravana', 'Peso', 'Categoria']].head(5), hide_index=True)

# --- GRÁFICOS ---
st.divider()
c1, c2 = st.columns(2)

with c1:
    st.markdown("### 📈 Distribución de Kilos")
    fig1 = px.histogram(df, x="Peso", color="Categoria", title="Campana de Gauss", 
                        color_discrete_sequence=['#2D5A27', '#5D4037', '#A89F91'])
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.markdown("### 💰 Distribución del Capital")
    fig2 = px.pie(df, values='Valor_ARS', names='Categoria', title="% Valor por Categoría",
                  color_discrete_sequence=['#2D5A27', '#5D4037', '#A89F91'], hole=.4)
    st.plotly_chart(fig2, use_container_width=True)


