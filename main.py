import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import os

# CONFIGURACIÓN ESTÉTICA
st.set_page_config(page_title="GI - Ganadería Inteligente", layout="wide", page_icon="🐂")

st.markdown("""
    <style>
    .main { background-color: #F8F9F3; }
    h1 { color: #2D5A27; font-family: 'Georgia', serif; font-size: 3.5rem; margin-bottom: 0px; }
    .sub { color: #5D4037; font-size: 1.2rem; margin-top: 0px; margin-bottom: 2rem; }
    .stMetric { border-left: 5px solid #2D5A27 !important; background-color: white; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("<h1>GANADERÍA INTELIGENTE</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub'>Bienvenido, Productor. Gestión autónoma de precisión.</p>", unsafe_allow_html=True)

# --- SIDEBAR: GESTIÓN DE DATOS Y CARGA ---
with st.sidebar:
    st.header("⚙️ Panel de Control")
    moneda = st.radio("Unidad de Medida", ["Pesos (ARS)", "Dólar MEP"], key="unit")
    
    st.divider()
    st.subheader("📥 Carga de Datos")
    
    # OPCIÓN 1: CARGA MASIVA
    archivo_subido = st.file_uploader("Subir archivo de pesada (.csv / .xlsx)", type=["csv", "xlsx"])
    
    # OPCIÓN 2: CARGA INDIVIDUAL (FORMULARIO)
    with st.expander("➕ Carga Manual Individual"):
        nueva_caravana = st.text_input("N° Caravana")
        nuevo_peso = st.number_input("Peso (kg)", min_value=0.0)
        nueva_cat = st.selectbox("Categoría", ["Ternero", "Novillito", "Novillo", "Vaca", "Vaquillona"])
        if st.button("Registrar Animal"):
            st.success(f"Animal {nueva_caravana} listo para procesar.")

    # OPCIÓN 3: GOOGLE SHEETS
    url_sheets = st.text_input("🔗 Link de Google Sheets (Opcional)")

    st.divider()
    st.subheader("💰 Precios del Día ($/kg)")
    p_nov = st.number_input("Novillito", value=5211.0)
    p_ter = st.number_input("Ternero", value=5650.0)
    p_vac = st.number_input("Vaca", value=2450.0)
    val_mep = 1433.0

# --- PROCESAMIENTO DE DATOS ---
# Prioridad: 1. Archivo subido, 2. Archivo en GitHub
archivo_base = 'datos_prueba_gi.csv'

if archivo_subido is not None:
    try:
        if archivo_subido.name.endswith('.csv'):
            df = pd.read_csv(archivo_subido)
        else:
            df = pd.read_excel(archivo_subido)
        st.sidebar.success("✅ Datos cargados correctamente.")
    except Exception as e:
        st.sidebar.error(f"Error al leer archivo: {e}")
        df = pd.read_csv(archivo_base) if os.path.exists(archivo_base) else None
elif url_sheets:
    # Lógica para leer Google Sheets (requiere que el link sea público o exportable)
    try:
        sheet_url = url_sheets.replace('/edit#gid=', '/export?format=csv&gid=')
        df = pd.read_csv(sheet_url)
    except:
        st.sidebar.warning("No se pudo leer el Sheets. Verifique permisos.")
        df = pd.read_csv(archivo_base) if os.path.exists(archivo_base) else None
else:
    # --- PROCESAMIENTO DE DATOS SEGURO ---
archivo_base = 'datos_prueba_gi.csv'

def cargar_datos_seguro(path):
    try:
        # Intentamos leer ignorando filas con errores y detectando el separador automáticamente
        return pd.read_csv(path, sep=None, engine='python', on_bad_lines='skip')
    except Exception as e:
        st.error(f"Error al leer la base de datos: {e}")
        return None

if archivo_subido is not None:
    # (Lógica para archivo subido igual que antes...)
    pass
else:
    # Esta es la línea que fallaba, ahora usa la función segura
    df = cargar_datos_seguro(archivo_base) if os.path.exists(archivo_base) else None

# --- DASHBOARD PRINCIPAL ---
if df is not None:
    df['Caravana'] = df['Caravana'].astype(str)
    
    col_izq, col_der = st.columns([1, 2.2])

    with col_izq:
        st.markdown("### 📊 Mi Rodeo")
        st.metric("Total Hacienda", f"{len(df)} Cabezas")
        
        # Conteo detallado
        st.write("---")
        conteo = df['Categoria'].value_counts()
        for cat, cant in conteo.items():
            st.write(f"**{cat}:** {cant}")
        
        st.divider()
        # Valuación
        def valuar(row):
            if "Ternero" in row['Categoria']: return row['Peso_Actual'] * p_ter
            if "Novillito" in row['Categoria']: return row['Peso_Actual'] * p_nov
            return row['Peso_Actual'] * p_vac
        
        df['Valor_Actual'] = df.apply(valuar, axis=1)
        v_total = df['Valor_Actual'].sum()
        
        if moneda == "Dólar MEP":
            st.metric("Capital en Pie", f"USD {(v_total/val_mep):,.0f}")
        else:
            st.metric("Capital en Pie", f"$ {v_total:,.0f}")

    with col_der:
        # LÓGICA DE VENTAS
        st.markdown("### 🚛 Oportunidades y Logística")
        listos = df[df['Peso_Actual'] >= 370]
        
        if len(listos) >= 30:
            st.success(f"🎯 **¡Jaula Lista!** Tenés {len(listos)} animales en peso de venta. Esto completa **{len(listos)//33} jaula(s)**.")
            
        else:
            st.info(f"Faltan {33 - len(listos)} animales para completar una jaula de 33 novillitos.")

        st.divider()
        # ANOMALÍAS
        st.markdown("### 🚨 Apartar (Anomalías)")
        media = df['Peso_Actual'].mean()
        std = df['Peso_Actual'].std()
        anomalias = df[df['Peso_Actual'] < (media - 2*std)]
        
        if not anomalias.empty:
            st.warning(f"Hay {len(anomalias)} animales con desvío crítico. Revisar en el próximo rejunte.")
            st.table(anomalias[['Caravana', 'Peso_Actual', 'Lote']].head(5))
        else:
            st.success("Rendimiento uniforme en todo el lote.")

    # GRÁFICO DE CAMPANA
    st.divider()
    st.markdown("### 📈 Distribución Estadística (Campana de Gauss)")
    fig = px.histogram(df, x="Peso_Actual", color="Categoria", marginal="rug", 
                       title="Dispersión de Kilos", color_discrete_sequence=['#2D5A27', '#5D4037', '#8D6E63'])
    st.plotly_chart(fig, use_container_width=True)
    

else:
    st.warning("⚠️ Sin datos disponibles. Subí un archivo o revisá el link de Sheets.")

