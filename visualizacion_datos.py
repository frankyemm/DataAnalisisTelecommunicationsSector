import streamlit as st
import pandas as pd
import plotly.express as px


def render_visualizacion_datos():
    st.title("Visualización de Datos de Telecomunicaciones")

    # CSS para centrar el contenido
    st.markdown(
        """
        <style>
        .center-content {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Selección del dataset
    datasets = {
        "Accesos por Rangos": "Data_cleaned/Accesos por rangos.csv",
        "Ingresos": "Data_cleaned/Ingresos.csv",
        "Penetración de Hogares": "Data_cleaned/Penetracion-hogares.csv",
        "Totales Accesos por Rango": "Data_cleaned/Totales Accesos por rango.csv",
        "Totales Accesos por Tecnología": "Data_cleaned/Totales Accesos Por Tecnología.csv",
        "Velocidad por Provincia": "Data_cleaned/Velocidad % por prov.csv",
        "Inflación Anual": "Data_cleaned/Inflacion_Anual_Argentina_2014_2024.csv",
    }

    dataset_name = st.selectbox("Selecciona un Dataset", list(datasets.keys()))
    file_path = datasets[dataset_name]

    # Cargar dataset seleccionado
    try:
        df = pd.read_csv(file_path)
        df = df[df["Año"] < 2024]  # Filtrar años menores a 2024

        # Opciones específicas para visualizaciones según el dataset
        st.subheader(f"Visualización: {dataset_name}")
        if dataset_name == "Accesos por Rangos":
            provincia = st.selectbox("Selecciona una Provincia", df["Provincia"].unique())
            año = st.selectbox("Selecciona un Año", df["Año"].unique())
            filtrar_y_graficar_accesos_por_rangos(df, provincia, año)

        elif dataset_name == "Ingresos":
            anio_inicio, anio_fin = st.slider(
                "Rango de Años",
                min_value=int(df["Año"].min()),
                max_value=int(df["Año"].max()),
                value=(2014, 2023),
            )
            graficar_ingresos_ajustados(df, anio_inicio, anio_fin)

        elif dataset_name == "Penetración de Hogares":
            provincia = st.selectbox("Selecciona una Provincia", df["Provincia"].unique())
            año = st.selectbox("Selecciona un Año", df["Año"].unique())
            graficar_penetracion_hogares(df, provincia, año)

        elif dataset_name == "Totales Accesos por Rango":
            año = st.selectbox("Selecciona un Año", df["Año"].unique())
            trimestre = st.selectbox("Selecciona un Trimestre", df["Trimestre"].unique())
            graficar_totales_accesos_por_rango(df, año, trimestre)

        elif dataset_name == "Totales Accesos por Tecnología":
            año = st.selectbox("Selecciona un Año", df["Año"].unique())
            trimestre = st.selectbox("Selecciona un Trimestre", df["Trimestre"].unique())
            graficar_totales_accesos_por_tecnologia(df, año, trimestre)

        elif dataset_name == "Velocidad por Provincia":
            provincia = st.selectbox("Selecciona una Provincia", df["Provincia"].unique())
            año = st.selectbox("Selecciona un Año", df["Año"].unique())
            graficar_velocidad_promedio(df, provincia, año)

        elif dataset_name == "Inflación Anual":
            anio_inicio, anio_fin = st.slider(
                "Rango de Años",
                min_value=int(df["Año"].min()),
                max_value=int(df["Año"].max()),
                value=(2014, 2023),
            )
            graficar_inflacion_anual(df, anio_inicio, anio_fin)

        # Mostrar dataset después de los gráficos
        st.subheader(f"Datos del Dataset: {dataset_name}")
        st.dataframe(df)

    except Exception as e:
        st.error(f"Error al cargar el dataset: {e}")


# Funciones de graficado específicas con centrado
def filtrar_y_graficar_accesos_por_rangos(df, provincia, año):
    df_filtrado = df[(df["Provincia"] == provincia) & (df["Año"] == año)]
    if not df_filtrado.empty:
        df_grouped = df_filtrado.groupby("Trimestre")["Total"].sum().reset_index()
        fig = px.bar(
            df_grouped,
            x="Trimestre",
            y="Total",
            text="Total",
            title=f"Distribución de Accesos por Rangos ({provincia}, {año})",
            color="Trimestre",
        )
        fig.update_traces(textposition="outside")
        st.markdown('<div class="center-content">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No hay datos disponibles para los filtros seleccionados.")


def graficar_ingresos_ajustados(df, anio_inicio, anio_fin):
    df_filtrado = df[(df["Año"] >= anio_inicio) & (df["Año"] <= anio_fin)]
    if not df_filtrado.empty:
        fig = px.line(
            df_filtrado,
            x="Año",
            y="Ingresos (miles de pesos)",
            title=f"Evolución de Ingresos Ajustados ({anio_inicio}-{anio_fin})",
        )
        st.markdown('<div class="center-content">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No hay datos disponibles para los filtros seleccionados.")


def graficar_penetracion_hogares(df, provincia, año):
    df_filtrado = df[(df["Provincia"] == provincia) & (df["Año"] == año)]
    if not df_filtrado.empty:
        fig = px.line(
            df_filtrado,
            x="Trimestre",
            y="Accesos por cada 100 hogares",
            title=f"Penetración de Hogares ({provincia}, {año})",
            markers=True,
        )
        st.markdown('<div class="center-content">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No hay datos disponibles para los filtros seleccionados.")


def graficar_totales_accesos_por_rango(df, año, trimestre):
    df_filtrado = df[(df["Año"] == año) & (df["Trimestre"] == trimestre)]
    if not df_filtrado.empty:
        categorias = df_filtrado.columns[2:]
        valores = df_filtrado.iloc[0, 2:]
        fig = px.bar(
            x=categorias,
            y=valores,
            labels={"x": "Rango", "y": "Total"},
            title=f"Totales de Accesos por Rango ({año}, Trimestre {trimestre})",
        )
        st.markdown('<div class="center-content">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No hay datos disponibles para los filtros seleccionados.")


def graficar_totales_accesos_por_tecnologia(df, año, trimestre):
    df_filtrado = df[(df["Año"] == año) & (df["Trimestre"] == trimestre)]
    if not df_filtrado.empty:
        categorias = df_filtrado.columns[2:]
        valores = df_filtrado.iloc[0, 2:]
        fig = px.bar(
            x=categorias,
            y=valores,
            labels={"x": "Tecnología", "y": "Total"},
            title=f"Totales de Accesos por Tecnología ({año}, Trimestre {trimestre})",
        )
        st.markdown('<div class="center-content">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No hay datos disponibles para los filtros seleccionados.")


def graficar_velocidad_promedio(df, provincia, año):
    df_filtrado = df[(df["Provincia"] == provincia) & (df["Año"] == año)]
    if not df_filtrado.empty:
        fig = px.line(
            df_filtrado,
            x="Trimestre",
            y="Mbps (Media de bajada)",
            title=f"Velocidad Promedio ({provincia}, {año})",
            markers=True,
        )
        st.markdown('<div class="center-content">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No hay datos disponibles para los filtros seleccionados.")


def graficar_inflacion_anual(df, anio_inicio, anio_fin):
    df_filtrado = df[(df["Año"] >= anio_inicio) & (df["Año"] <= anio_fin)]
    if not df_filtrado.empty:
        fig = px.line(
            df_filtrado,
            x="Año",
            y="Inflación Anual (%)",
            title=f"Inflación Anual ({anio_inicio}-{anio_fin})",
            markers=True,
        )
        st.markdown('<div class="center-content">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No hay datos disponibles para los filtros seleccionados.")
