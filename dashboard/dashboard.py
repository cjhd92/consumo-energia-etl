import streamlit as st
import pandas as pd
import duckdb
import os
import sys
import altair as alt

# Añadir la carpeta raíz al path para importar scripts
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Importar funciones ETL
from scripts.extract import extract_data
from scripts.transform import transform_data
from scripts.load_duckdb import load_to_duckdb

# Configuración general
st.set_page_config(page_title="Consumo Energético", layout="wide")
st.title("⚡ Panel de Control - Consumo Eléctrico")

# Sidebar: ejecución ETL
st.sidebar.title("🔄 Ejecución del ETL")

if st.sidebar.button("1️⃣ Descargar datos"):
    try:
        extract_data()
        st.sidebar.success("✅ Datos descargados correctamente.")
    except Exception as e:
        st.sidebar.error(f"❌ Error en la descarga: {e}")

if st.sidebar.button("2️⃣ Transformar datos"):
    try:
        transform_data()
        st.sidebar.success("✅ Datos transformados correctamente.")
    except Exception as e:
        st.sidebar.error(f"❌ Error en la transformación: {e}")

if st.sidebar.button("3️⃣ Cargar a DuckDB"):
    try:
        load_to_duckdb()
        st.sidebar.success("✅ Datos cargados en DuckDB.")
    except Exception as e:
        st.sidebar.error(f"❌ Error en la carga: {e}")

# Visualización (si existe la base de datos)
db_path = "data/consumo.duckdb"

if os.path.exists(db_path):
    con = duckdb.connect(db_path)
    tables = con.execute("SHOW TABLES").fetchdf()

    if "consumo_energia" in tables["name"].values:
        df = con.execute("SELECT * FROM consumo_energia").fetchdf()
        con.close()

        df["fecha"] = pd.to_datetime(df["fecha"])

        # Filtros en la barra lateral
        st.sidebar.title("🎛️ Filtros de visualización")
        fuente = st.sidebar.selectbox("Fuente principal", sorted(df["fuente_principal"].unique()))

        fechas = st.sidebar.date_input(
            "Rango de fechas",
            [df["fecha"].min(), df["fecha"].max()]
        )

        regiones = st.sidebar.multiselect(
            "Selecciona hasta 2 regiones para comparar",
            sorted(df["region"].unique()),
            default=sorted(df["region"].unique())[:2]
        )

        # Validación de filtros
        if len(regiones) != 2:
            st.warning("⚠️ Selecciona exactamente dos regiones para comparar.")
        else:
            fecha_ini, fecha_fin = fechas
            df = df[(df["fecha"] >= pd.to_datetime(fecha_ini)) & (df["fecha"] <= pd.to_datetime(fecha_fin))]
            df = df[df["fuente_principal"] == fuente]

            df_r1 = df[df["region"] == regiones[0]].copy()
            df_r2 = df[df["region"] == regiones[1]].copy()

            st.subheader("📊 Comparación de Consumo Eléctrico por Región")

            col1, col2 = st.columns(2)

            col1.metric(
                f"{regiones[0]} - Consumo Medio",
                f"{df_r1['consumo_mwh'].mean():,.0f} MWh"
            )
            col2.metric(
                f"{regiones[1]} - Consumo Medio",
                f"{df_r2['consumo_mwh'].mean():,.0f} MWh"
            )

            col1.metric(
                f"{regiones[0]} - Precio Promedio",
                f"{df_r1['precio_eur_mwh'].mean():.2f} €/MWh"
            )
            col2.metric(
                f"{regiones[1]} - Precio Promedio",
                f"{df_r2['precio_eur_mwh'].mean():.2f} €/MWh"
            )

            # Gráfico comparativo
            df_plot = pd.concat([df_r1, df_r2])
            df_plot["region"] = df_plot["region"].astype(str)

            chart = alt.Chart(df_plot).mark_line().encode(
                x='fecha:T',
                y='consumo_mwh:Q',
                color='region:N',
                tooltip=['region', 'fecha:T', 'consumo_mwh']
            ).properties(
                title="Evolución del consumo MWh por región",
                width=1000,
                height=400
            )

            st.altair_chart(chart, use_container_width=True)

            # Tabla expandible
            with st.expander("📄 Ver tabla comparativa"):
                st.dataframe(df_plot)

    else:
        st.warning("⚠️ La tabla 'consumo_energia' no existe. Ejecuta primero los pasos ETL.")
else:
    st.info("ℹ️ Ejecuta los pasos de carga para crear la base de datos.")
