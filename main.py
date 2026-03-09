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
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# CONFIGURACIÓN ESTÉTICA Y DE PÁGINA
st.set_page_config(page_title="GI - Ganadería Inteligente", layout="wide", page_icon="🐂")

# Estilos CSS Personalizados (Minimalismo de Campo)
st.markdown("""
    <style>
    .main { background-color: #F8F9F3; } /* Fondo Arena muy claro */
    .stMetric { background-color: #FFFFFF; padding: 20px; border-radius: 12px; border-left: 6px solid #2D5A27; box-shadow: 2px 2px 8px rgba(0,0,0,0.08); }
    h1, h2, h3 { color: #2D5A27; font-family: 'Helvetica Neue', sans-serif; } /* Verde Monte */
    .css-10trblm { color: #5D4037; } /* Color de texto secundario */
    .stButton>button { background-color: #2D5A27; color: white; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO PRINCIPAL (HEADER) ---
# Simulación del logo (esto se puede reemplazar por una imagen real con st.image)
col_logo, col_titulo = st.columns([1, 6])
with col_logo:
    # Usamos un emoji y texto estilizado como logo temporal
    st.markdown("<h1 style='text-align: center; color: #5D4037; font-size: 60px;'>GI</h1>", unsafe_allow_html=True)
with col_titulo:
    st.title("GANADERÍA INTELIGENTE")
    st.subheader("Optimización Bioeconómica - Reconquista, Santa Fe")

st.divider()

# --- SIDEBAR (MENÚ LATERAL DE GESTIÓN) ---
with st.sidebar:
    st.markdown("## ⚙️ Configuración")
    
    # 1. Moneda y Precios (Base: Marzo 2026)
    moneda = st.radio("Unidad de Medida", ["Pesos (ARS)", "Dólar MEP"])
    
    # Precios simulados por defecto (pueden ser automáticos a futuro)
    precios_base = {"Novillito": 5211.0, "Ternero": 5600.0, "MEP": 1433.0}
    
    precio_nov = st.number_input("Precio Novillito ($/kg)", value=precios_base["Novillito"])
    precio_ternero = st.number_input("Precio Ternero ($/kg)", value=precios_base["Ternero"])
    mep = precios_base["MEP"]

    # 2. Buscador RFID
    st.markdown("---")
    caravana_busqueda = st.text_input("🔍 Buscar Caravana RFID (15 dígitos)")

# --- CARGA DE DATOS (DOCUMENTO DE PRUEBA) ---
# Intentamos cargar el archivo, si no existe, mostramos mensaje
archivo_datos = 'datos_prueba_gi.csv'
if os.path.exists(archivo_datos):
    df = pd.read_csv(archivo_datos)
    # Aseguramos formato de caravana y fechas
    df['Caravana'] = df['Caravana'].astype(str)
    df['Fecha_Pesada'] = pd.to_datetime(df['Fecha_Pesada'])
    
    # --- CÁLCULOS DEL MOTOR ---
    total_animales = len(df)
    # GMD Media (Asumimos última pesada vs la anterior si existe, o esperada)
    gmd_media = df['GMD_Esperada'].mean() # Simplificación para la demo
    
    # Valor del Rodeo
    df['Valor_Actual'] = df['Peso_Actual'] * precio_nov # Simplificación: todo a precio Novillito
    valor_rodeo_total = df['Valor_Actual'].sum()

    # --- PANTALLA PRINCIPAL (DASHBOARD) ---
    # 1. KPIs (Tarjetas de Métricas)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="👥 Población Total", value=f"{total_animales} Cabezas")
    with col2:
        st.metric(label="📈 GMD Media Estimada", value=f"{gmd_media:.3f} kg/día", delta="0.010 kg vs mes ant.")
    with col3:
        if moneda == "Dólar MEP":
            st.metric(label="💰 Valor del Rodeo", value=f"USD {(valor_rodeo_total/mep):,.0f}")
        else:
            st.metric(label="💰 Valor del Rodeo", value=f"$ {valor_rodeo_total:,.0f}")

    st.write("---")

    # 2. Anomalías y Consejos (Z-Score > 2 desvíos)
    media_peso = df['Peso_Actual'].mean()
    desvio_peso = df['Peso_Actual'].std()
    
    # Identificar Anomalías Negativas
    anomalias = df[df['Peso_Actual'] < (media_peso - 2 * desvio_peso)]
    
    st.markdown("### 🚨 Panel de Alertas y Oportunidades")
    
    if not anomalias.empty:
        st.error(f"⚠️ **Atención:** Se detectaron {len(anomalias)} animales con bajo rendimiento (Anomalías Negativas).")
        st.write(anomalias[['Caravana', 'Peso_Actual', 'Lote']])
        st.markdown("*Recomendación: Apartar en el próximo rejunte para revisión sanitaria.*")
    else:
        st.success("✅ No se detectaron anomalías significativas en el peso actual.")

    # 3. Gráficos y Tablas
    st.write("---")
    tab1, tab2 = st.tabs(["📋 Inventario Completo", "📊 Distribución de Pesos"])
    
    with tab1:
        st.dataframe(df.style.background_gradient(cmap='YlGn', subset=['Peso_Actual']), use_container_width=True)
    
    with tab2:
        # Gráfico de Campana de Gauss (Distribución Normal)
        fig_dist = px.histogram(df, x="Peso_Actual", nbins=20, title="Distribución de Pesos del Rodeo", 
                               labels={'Peso_Actual': 'Peso (kg)'}, color_discrete_sequence=['#2D5A27'])
        # Líneas de media y desvíos
        fig_dist.add_vline(x=media_peso, line_dash="dash", line_color="#5D4037", annotation_text="Media")
        fig_dist.add_vline(x=media_peso - 2*desvio_peso, line_color="#ff4b4b", annotation_text="-2s")
        st.plotly_chart(fig_dist, use_container_width=True)

else:
    # Mensaje si no hay archivo de datos
    st.warning("⚠️ No se encontró el archivo de datos `datos_prueba_gi.csv`. Por favor, subilo a GitHub para ver la App funcionando.")
    st.info("💡 Podés usar el código de abajo para generar un archivo de prueba.")

# --- BÚSQUEDA RFID ---
if caravana_busqueda and os.path.exists(archivo_datos):
    animal = df[df['Caravana'] == caravana_busqueda]
    if not animal.empty:
        st.sidebar.markdown("---")
        st.sidebar.success(f"📍 Ficha del Animal: {caravana_busqueda}")
        st.sidebar.write(animal.iloc[0])
    else:
        st.sidebar.error("❌ Animal no encontrado.")
with tab2:
    st.write("🚛 **Transporte sugerido:** Semirremolque Jaula (1 Piso)")
    st.write("Carga actual: 32 Novillitos + 3 Terneros de bajo rendimiento (Relleno).")

