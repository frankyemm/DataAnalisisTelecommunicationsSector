import streamlit as st
from visualizacion_datos import render_visualizacion_datos
from A_KPIs import render_kpi_analysis

def main():
    # Inicializar valores en el estado de la sesión
    if "page" not in st.session_state:
        st.session_state["page"] = "home"
    if "selected_dataset" not in st.session_state:
        st.session_state["selected_dataset"] = None

    # Configuración inicial
    st.set_page_config(
        page_title="Dashboard Telecomunicaciones",
        layout="wide"
    )

    # Selector de tema (Claro/Oscuro)
    theme = st.radio("Selecciona un tema", options=["Claro", "Oscuro"], index=1, horizontal=True)

    # Aplicar estilos CSS dinámicamente según el tema seleccionado
    if theme == "Oscuro":
        st.markdown(
            """
            <style>
            :root {
                --primary-color: #1f77b4;
                --background-color: #0e1117;
                --secondary-background-color: #262730;
                --text-color: #fafafa;
            }

            .css-1d391kg {  /* Fondo principal */
                background-color: var(--background-color) !important;
            }
            .css-1cpxqw2 {  /* Texto */
                color: var(--text-color) !important;
            }
            .css-1gnykxp, .css-1gynld6 {  /* Fondos secundarios */
                background-color: var(--secondary-background-color) !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <style>
            :root {
                --primary-color: #1f77b4;
                --background-color: #ffffff;
                --secondary-background-color: #f0f2f6;
                --text-color: #000000;
            }

            .css-1d391kg {  /* Fondo principal */
                background-color: var(--background-color) !important;
            }
            .css-1cpxqw2 {  /* Texto */
                color: var(--text-color) !important;
            }
            .css-1gnykxp, .css-1gynld6 {  /* Fondos secundarios */
                background-color: var(--secondary-background-color) !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

    # Barra lateral de navegación
    st.title("Bienvenido al Análisis del Sector de Telecomunicaciones en Argentina")
    st.write("""
        Este proyecto tiene como objetivo analizar el comportamiento del sector de telecomunicaciones 
        en Argentina utilizando datos relevantes sobre velocidad de internet, penetración de hogares conectados, 
        tecnologías utilizadas y métricas financieras ajustadas por inflación.\n
        ¿Qué te gustaría observar?
    """)

    # Botones de navegación rápida
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Ir a Análisis de KPIs"):
            st.session_state["page"] = "A_KPIs"

    with col2:
        if st.button("Ir a Visualización de Datos"):
            st.experimental_set_query_params(page="visualizacion_datos")
            st.session_state["page"] = "visualizacion_datos"

    with col3:
        if st.button("Volver a Home"):
            st.session_state["page"] = "home"

    # Detectar la página actual a través de los parámetros de la URL
    if st.session_state["page"] == "A_KPIs":
        render_kpi_analysis()
    elif st.session_state["page"] == "visualizacion_datos":
        render_visualizacion_datos()
    else:
        render_home_page()

    # Desglose de los KPIs
    st.header("KPIs Analizados")
    st.subheader("KPI 1: Penetración de accesos por hogares")
    st.markdown("""
    **Fórmula:**
    
    $KPI = \\left(\\frac{\\text{Nuevo acceso} - \\text{Acceso actual}}{\\text{Acceso actual}}\\right) \\times 100$

    **Variables necesarias:**
    - **Acceso actual:** Accesos por cada 100 hogares en el trimestre actual.
    - **Nuevo acceso:** Proyección del número de accesos por cada 100 hogares tras el incremento del 2%.

    **Descripción:** Evalúa el crecimiento porcentual de accesos en hogares durante los trimestres 3 y 4 del 2023.

    **Resultados:**
    - Crecimiento positivo en provincias como Buenos Aires y Córdoba.
    - Provincias rurales muestran menor penetración.

    **Recomendaciones:**
    - Invertir en áreas rurales para reducir la brecha digital.
    - Promover políticas públicas que incentiven el acceso.
    """)

    st.subheader("KPI 2: Velocidad promedio de internet")
    st.markdown("""
    **Fórmula:**

    $KPI = \\left(\\frac{\\text{Nueva velocidad promedio} - \\text{Velocidad promedio actual}}{\\text{Velocidad promedio actual}}\\right) \\times 100$


    **Variables necesarias:**
    - **Velocidad promedio actual:** Media de las velocidades actuales por provincia (Mbps).
    - **Nueva velocidad promedio:** Proyección de la velocidad promedio tras el incremento del 2%.

    **Descripción:** Analiza el incremento en Mbps promedio en las provincias entre los trimestres 3 y 4 del 2023.

    **Resultados:**
    - Capital Federal lidera con velocidades superiores a 180 Mbps.
    - Regiones menos urbanizadas presentan velocidades más bajas.

    **Recomendaciones:**
    - Expandir la infraestructura de fibra óptica en regiones con velocidades bajas.
    - Incentivar a las ISPs a mantener estándares elevados de calidad.
    """)

    st.subheader("KPI 3: Cobertura de fibra óptica")
    st.markdown("""
    **Fórmula:**

    $KPI = \\left(\\frac{\\text{Total Accesos proyectados} - \\text{Total Accesos actuales}}{\\text{Total Accesos actuales}}\\right) \\times 100$


    **Variables necesarias:**
    - **Accesos actuales:** Total de accesos por tecnologías (Fibra Óptica) en el trimestre actual.
    - **Ingresos proyectados:** Proyección de accesos por tecnologías (Fibra Óptica) con un incremento del 1.5%.

    **Descripción:** Mide el crecimiento de accesos por fibra óptica en los trimestres 3 y 4 del 2023.

    **Resultados:**
    - Incrementos significativos en provincias como Mendoza y Córdoba.
    - ADSL y tecnologías obsoletas aún tienen presencia considerable.

    **Recomendaciones:**
    - Enfocarse en la transición de ADSL a fibra óptica.
    - Expandir la cobertura en zonas suburbanas y rurales.
    """)


def render_home_page():
    st.header("Inicio")
    st.write("Selecciona una página para continuar.")


if __name__ == "__main__":
    main()
