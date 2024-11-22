import streamlit as st
import pandas as pd
import plotly.express as px


class KPIAnalyzerStreamlit:
    def __init__(self, df_penetracion, df_velocidad, df_fibra):
        """
        Inicializa la clase para calcular y graficar los tres KPI.

        Args:
            df_penetracion (pd.DataFrame): DataFrame para el KPI de penetración.
            df_velocidad (pd.DataFrame): DataFrame para el KPI de velocidad.
            df_fibra (pd.DataFrame): DataFrame para el KPI de fibra óptica.
        """
        self.df_penetracion = df_penetracion
        self.df_velocidad = df_velocidad
        self.df_fibra = df_fibra[df_fibra["Año"] < 2024]

        # Umbrales mínimos para los KPIs
        self.umbral_penetracion = 2.0  # 2% de crecimiento
        self.umbral_velocidad = 2.0   # 2% de crecimiento
        self.umbral_fibra = 1.5       # 1.5% de crecimiento

    def crear_tarjeta(self, crecimiento, umbral):
        """
        Crea una tarjeta rectangular con el resultado del KPI.

        Args:
            crecimiento (float): Valor del crecimiento.
            umbral (float): Umbral mínimo para cumplir el KPI.

        Returns:
            str: HTML para renderizar la tarjeta.
        """
        color = "#66ff79" if crecimiento >= umbral else "#ff6565"
        flecha = "▲" if crecimiento >= 0 else "▼"
        return f"""
        <div style="
            background-color: {color};
            padding: 15px;
            border-radius: 10px;
            width: 300px;
            margin: 10px auto;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            color: #000000;
        ">
            {flecha} {crecimiento:.2f}%
        </div>
        """

    def calcular_y_graficar_penetracion(self, provincia):
        df_filtrado = self.df_penetracion[
            (self.df_penetracion["Año"] == 2023) & 
            (self.df_penetracion["Provincia"] == provincia) & 
            (self.df_penetracion["Trimestre"].isin([3, 4]))
        ]
        if not df_filtrado.empty:
            df_filtrado = df_filtrado.sort_values(by=["Trimestre"])
            crecimiento = (
                df_filtrado["Accesos por cada 100 hogares"].iloc[-1] -
                df_filtrado["Accesos por cada 100 hogares"].iloc[-2]
            ) / df_filtrado["Accesos por cada 100 hogares"].iloc[-2] * 100

            grafico_df = pd.DataFrame({
                "Etiqueta": ["Crecimiento Último Trimestre"],
                "Valor": [crecimiento]
            })
            fig = self.graficar_barras_simplificado(
                grafico_df,
                "Etiqueta",
                "Valor",
                f"KPI - Penetración Provincia {provincia}"
            )
            
            tarjeta = self.crear_tarjeta(crecimiento, self.umbral_penetracion)
            return tarjeta, fig

    def calcular_y_graficar_velocidad(self, provincia):
        df_filtrado = self.df_velocidad[
            (self.df_velocidad["Año"] == 2023) & 
            (self.df_velocidad["Provincia"] == provincia) & 
            (self.df_velocidad["Trimestre"].isin([3, 4]))
        ]
        if not df_filtrado.empty:
            df_filtrado = df_filtrado.sort_values(by=["Trimestre"])
            crecimiento = (
                df_filtrado["Mbps (Media de bajada)"].iloc[-1] -
                df_filtrado["Mbps (Media de bajada)"].iloc[-2]
            ) / df_filtrado["Mbps (Media de bajada)"].iloc[-2] * 100

            grafico_df = pd.DataFrame({
                "Etiqueta": ["Crecimiento Último Trimestre"],
                "Valor": [crecimiento]
            })
            fig = self.graficar_barras_simplificado(
                grafico_df,
                "Etiqueta",
                "Valor",
                f"KPI - Velocidad Promedio Provincia {provincia}"
            )
            
            tarjeta = self.crear_tarjeta(crecimiento, self.umbral_velocidad)
            return tarjeta, fig

    def calcular_y_graficar_fibra(self):
        # Filtrar datos por años y ordenar
        anio_min = int(self.df_fibra["Año"].min())
        anio_max = int(self.df_fibra["Año"].max())
        
        # Añadir selector de rango de años en la interfaz
        rango_seleccionado = st.slider(
            "Selecciona un rango de años",
            min_value=anio_min,
            max_value=anio_max,
            value=(anio_min, anio_max),
            step=1
        )
        
        # Filtrar datos por el rango seleccionado
        df_filtrado = self.df_fibra[
            (self.df_fibra["Año"] >= rango_seleccionado[0]) & 
            (self.df_fibra["Año"] <= rango_seleccionado[1])
        ].sort_values(by=["Año", "Trimestre"])
        
        # Calcular el crecimiento para cada trimestre dentro del rango
        df_filtrado["Crecimiento (%)"] = df_filtrado["Fibra óptica"].pct_change() * 100

        # Filtrar para eliminar valores NaN que resultan de pct_change
        df_filtrado = df_filtrado.dropna(subset=["Crecimiento (%)"])

        if not df_filtrado.empty:
            # Crear un DataFrame para graficar el histórico
            grafico_df = df_filtrado[["Año", "Trimestre", "Crecimiento (%)"]]
            grafico_df["Periodo"] = grafico_df["Año"].astype(str) + " Q" + grafico_df["Trimestre"].astype(str)

            # Crear gráfico de línea para el histórico
            fig = px.line(
                grafico_df,
                x="Periodo",
                y="Crecimiento (%)",
                title=f"KPI Histórico - Cobertura Fibra Óptica ({rango_seleccionado[0]}-{rango_seleccionado[1]})",
                markers=True
            )
            fig.update_layout(xaxis_title="Período", yaxis_title="Crecimiento (%)")

            # Calcular el crecimiento más reciente para la tarjeta
            crecimiento_reciente = grafico_df["Crecimiento (%)"].iloc[-1]
            tarjeta = self.crear_tarjeta(crecimiento_reciente, self.umbral_fibra)
            
            return tarjeta, fig
        else:
            # Retornar mensaje de error si no hay datos suficientes
            st.warning(f"No hay datos suficientes para el rango seleccionado ({rango_seleccionado[0]}-{rango_seleccionado[1]}).")
            return None, None



    def graficar_barras_simplificado(self, df, x_col, y_col, title):
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            text=y_col,
            title=title,
            labels={x_col: x_col, y_col: y_col},
        )
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Crecimiento (%)",
            xaxis=dict(type="category")
        )
        return fig

    def display(self):
        st.title("Análisis de KPIs de Telecomunicaciones")
        kpi_options = ["Penetración", "Velocidad Promedio", "Cobertura Fibra Óptica"]
        kpi = st.selectbox("Selecciona un KPI", kpi_options)
        
        tarjeta = None
        fig = None
        if kpi in ["Penetración", "Velocidad Promedio"]:
            provincia = st.selectbox("Selecciona una Provincia", self.df_penetracion["Provincia"].unique())
            if kpi == "Penetración":
                tarjeta, fig = self.calcular_y_graficar_penetracion(provincia)
            else:
                tarjeta, fig = self.calcular_y_graficar_velocidad(provincia)
        elif kpi == "Cobertura Fibra Óptica":
            tarjeta, fig = self.calcular_y_graficar_fibra()
        
        # Renderizar primero la tarjeta
        if tarjeta:
            st.markdown(tarjeta, unsafe_allow_html=True)
        # Luego renderizar el gráfico
        if fig:
            st.plotly_chart(fig, use_container_width=True)
