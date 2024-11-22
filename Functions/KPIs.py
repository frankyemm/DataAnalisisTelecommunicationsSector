import pandas as pd
import plotly.express as px
from ipywidgets import widgets, interactive_output
from IPython.display import display
import plotly.io as pio

pio.renderers.default = "notebook"  # Renderiza directamente en el notebook



class KPIAnalyzer:
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
        self.df_fibra = df_fibra[df_fibra["Año"] < 2024]  # Filtrar años menores a 2024

        # Widgets de selección general
        self.kpi_selector = widgets.Dropdown(
            options=["Penetración", "Velocidad Promedio", "Cobertura Fibra Óptica"],
            description="KPI:"
        )
        self.provincia_widget = widgets.Dropdown(
            options=self.df_penetracion["Provincia"].unique(),
            description="Provincia:"
        )

        # Conexión del widget con la función de cálculo y visualización
        self.output = interactive_output(
            self._graficar_kpi,
            {
                "kpi": self.kpi_selector,
                "provincia": self.provincia_widget,
            }
        )

    def _calcular_y_graficar_penetracion(self, provincia):
        """
        Calcula y grafica el KPI de penetración.
        """
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

            # Crear DataFrame para graficar
            grafico_df = pd.DataFrame({
                "Etiqueta": ["Crecimiento Último Trimestre"],
                "Valor": [crecimiento]
            })
            self._graficar_barras_simplificado(
                grafico_df,
                "Etiqueta",
                "Valor",
                f"KPI - Penetración Provincia {provincia}"
            )

    def _calcular_y_graficar_velocidad(self, provincia):
        """
        Calcula y grafica el KPI de velocidad promedio.
        """
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

            # Crear DataFrame para graficar
            grafico_df = pd.DataFrame({
                "Etiqueta": ["Crecimiento Último Trimestre"],
                "Valor": [crecimiento]
            })
            self._graficar_barras_simplificado(
                grafico_df,
                "Etiqueta",
                "Valor",
                f"KPI - Velocidad Promedio Provincia {provincia}"
            )


    def _calcular_y_graficar_fibra(self):
        # Determinar el rango de años en los datos
        anio_min = int(self.df_fibra["Año"].min())
        anio_max = int(self.df_fibra["Año"].max())

        # Crear un slider para seleccionar el rango de años
        rango_slider = widgets.IntRangeSlider(
            value=(anio_min, anio_max),
            min=anio_min,
            max=anio_max,
            step=1,
            description='Años:',
            continuous_update=False,
        )
        display(rango_slider)

        def on_value_change(change):
            rango_seleccionado = change['new']
            
            # Filtrar datos según el rango seleccionado
            df_filtrado = self.df_fibra[
                (self.df_fibra["Año"] >= rango_seleccionado[0]) & 
                (self.df_fibra["Año"] <= rango_seleccionado[1])
            ].sort_values(by=["Año", "Trimestre"])

            # Calcular el crecimiento porcentual trimestral
            df_filtrado["Crecimiento (%)"] = df_filtrado["Fibra óptica"].pct_change() * 100
            df_filtrado = df_filtrado.dropna(subset=["Crecimiento (%)"])

            if not df_filtrado.empty:
                # Crear un DataFrame para graficar
                grafico_df = df_filtrado[["Año", "Trimestre", "Crecimiento (%)"]].copy()
                grafico_df["Periodo"] = grafico_df["Año"].astype(str) + " Q" + grafico_df["Trimestre"].astype(str)

                # Crear gráfico de línea
                import plotly.express as px
                fig = px.line(
                    grafico_df,
                    x="Periodo",
                    y="Crecimiento (%)",
                    title=f"KPI Histórico - Cobertura Fibra Óptica ({rango_seleccionado[0]}-{rango_seleccionado[1]})",
                    markers=True
                )
                fig.update_layout(xaxis_title="Período", yaxis_title="Crecimiento (%)")

                # Mostrar el gráfico
                fig.show()
            else:
                print("No hay datos suficientes para el rango seleccionado.")
        
        # Vincular el slider al evento de cambio
        rango_slider.observe(on_value_change, names='value')




    def _graficar_barras_simplificado(self, df, x_col, y_col, title):
        """
        Genera un gráfico de barras simplificado con una sola barra.

        Args:
            df (pd.DataFrame): DataFrame con los datos calculados.
            x_col (str): Columna para el eje X.
            y_col (str): Columna para el eje Y.
            title (str): Título del gráfico.
        """
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
        fig.show()

    def _graficar_kpi(self, kpi, provincia):
        """
        Llama a la función correspondiente para graficar el KPI seleccionado.
        """
        if kpi == "Penetración":
            self._calcular_y_graficar_penetracion(provincia)
        elif kpi == "Velocidad Promedio":
            self._calcular_y_graficar_velocidad(provincia)
        elif kpi == "Cobertura Fibra Óptica":
            self._calcular_y_graficar_fibra()

    def display(self):
        """
        Muestra los widgets y el gráfico interactivo.
        """
        display(
            widgets.VBox([
                self.kpi_selector,
                widgets.HBox([self.provincia_widget]),
                self.output
            ])
        )
