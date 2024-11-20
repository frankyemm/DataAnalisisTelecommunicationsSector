import pandas as pd
import plotly.graph_objects as go
from IPython.display import display
from ipywidgets import widgets, Output, HBox, VBox, interactive_output
import plotly.express as px


class AccesosPorRangosPlot:
    def __init__(self, df):
        """
        Inicializa la clase con el DataFrame y configura los widgets.
        
        Args:
            df (pd.DataFrame): DataFrame que contiene los datos de accesos por rangos.
        """
        self.df = df
        self.output = Output()
        self.colores = ["blue", "orange", "green", "red"]
        
        # Crear los widgets de selección
        self.provincia_widget = widgets.Dropdown(
            options=self.df["Provincia"].unique(),
            description="Provincia:"
        )
        self.año_widget = widgets.Dropdown(
            options=self.df["Año"].unique(),
            description="Año:"
        )
        
        # Conectar los widgets con el método de actualización
        self.provincia_widget.observe(self.actualiza_output, names="value")
        self.año_widget.observe(self.actualiza_output, names="value")
        
    def graficar_accesos(self, provincia, año):
        """
        Filtra el DataFrame y genera un gráfico interactivo con los datos seleccionados.
        
        Args:
            provincia (str): Provincia seleccionada.
            año (int): Año seleccionado.
        """
        df_filtrado = self.df[
            (self.df["Provincia"] == provincia) & 
            (self.df["Año"] == año)
        ]
        
        # Crear la gráfica
        fig = go.Figure()
        if not df_filtrado.empty:
            # Sumar los valores por trimestre
            df_grouped = df_filtrado.groupby("Trimestre")["Total"].sum().reset_index()
            

            fig.add_trace(
                go.Bar(
                    x=df_grouped["Trimestre"],  # Eje x: Trimestres
                    y=df_grouped["Total"],      # Eje y: Total
                    name="Total",
                    text=df_grouped["Total"],  # Agregar texto con los valores
                    textposition="outside",    # Posición del texto (encima de las barras)
                    marker_color=self.colores[:len(df_grouped)],
                )
            )
            fig.update_layout(
                title=f"Distribución de Accesos Totales por Trimestre en {provincia} ({año})",
                xaxis_title="Trimestre",
                yaxis_title="Total",
                xaxis=dict(type="category"),  # Asegurar categorías en el eje x
            )
        else:
            fig.add_annotation(
                text="No hay datos para los filtros seleccionados.",
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=16, color="red")
            )
        fig.show()

    def actualiza_output(self, *args):
        """
        Actualiza el gráfico en función de los valores seleccionados en los widgets.
        """
        with self.output:
            self.output.clear_output(wait=True)  # Refresca la salida en lugar de acumular gráficos
            self.graficar_accesos(
                self.provincia_widget.value,
                self.año_widget.value
            )

    def display(self):
        """
        Muestra los widgets y el área de salida del gráfico.
        """
        display(VBox([HBox([self.provincia_widget, self.año_widget]), self.output]))


class DistribucionAccesos:
    def __init__(self, df):
        """
        Inicializa la clase con el DataFrame y configura los widgets.
        
        Args:
            df (pd.DataFrame): DataFrame que contiene los datos de accesos por velocidades.
        """
        self.df = df
        
        # Crear los widgets de selección
        self.provincia_widget = widgets.Dropdown(
            options=self.df["Provincia"].unique(),
            description="Provincia:"
        )
        self.año_widget = widgets.Dropdown(
            options=self.df["Año"].unique(),
            description="Año:"
        )
        self.trimestre_widget = widgets.Dropdown(
            options=self.df["Trimestre"].unique(),
            description="Trimestre:"
        )
        
        # Conectar los widgets con la función interactiva
        self.output = interactive_output(
            self.graficar_distribucion,
            {
                "provincia": self.provincia_widget,
                "año": self.año_widget,
                "trimestre": self.trimestre_widget
            }
        )
    
    def graficar_distribucion(self, provincia, año, trimestre):
        """
        Filtra el DataFrame y genera un gráfico interactivo con los datos seleccionados.
        
        Args:
            provincia (str): Provincia seleccionada.
            año (int): Año seleccionado.
            trimestre (str): Trimestre seleccionado.
        """
        df_filtrado = self.df[
            (self.df["Provincia"] == provincia) &
            (self.df["Año"] == año) &
            (self.df["Trimestre"] == trimestre)
        ]
        
        if not df_filtrado.empty:
            # Transformar los datos para la visualización (de columnas a filas)
            df_melted = df_filtrado.melt(
                id_vars=["Provincia", "Año", "Trimestre"],
                value_vars=[
                    "HASTA 512 kbps", "+ 512 Kbps - 1 Mbps", "+ 1 Mbps - 6 Mbps",
                    "+ 6 Mbps - 10 Mbps", "+ 10 Mbps - 20 Mbps", "+ 20 Mbps - 30 Mbps",
                    "+ 30 Mbps", "OTROS"
                ],
                var_name="Velocidad",
                value_name="Accesos"
            )
            
            # Crear gráfico de barras apiladas
            fig = px.bar(
                df_melted,
                x="Velocidad",
                y="Accesos",
                color="Velocidad",
                title=f"Distribución de Accesos por Velocidades en {provincia} ({trimestre} {año})",
                labels={"Accesos": "Cantidad de Accesos", "Velocidad": "Rango de Velocidades"},
                text="Accesos"
            )
            fig.update_traces(textposition="outside")
            fig.show()
        else:
            print("No hay datos disponibles para los filtros seleccionados.")
    
    def display(self):
        """
        Muestra los widgets y el área de salida del gráfico.
        """
        display(widgets.VBox([widgets.HBox([self.provincia_widget, self.año_widget, self.trimestre_widget]), self.output]))
        

class IngresosInflacion:
    def __init__(self, df_ingresos, df_inflacion_anual, anio_base=2014):
        """
        Inicializa la clase con los DataFrames de ingresos e inflación anual.
        
        Args:
            df_ingresos (pd.DataFrame): DataFrame con columnas Año, Trimestre, Ingresos (miles de pesos), Periodo.
            df_inflacion_anual (pd.DataFrame): DataFrame con columnas Año, Inflación Anual (%).
            anio_base (int): Año base para ajustar los ingresos por inflación (default: 2014).
        """
        self.df_ingresos = df_ingresos
        self.df_inflacion_anual = df_inflacion_anual
        self.anio_base = anio_base
        
        # Ajustar ingresos por inflación
        self.df_ajustado = self._ajustar_ingresos_por_inflacion()
    
    def _ajustar_ingresos_por_inflacion(self):
        """
        Ajusta los ingresos por inflación utilizando el año base.
        
        Returns:
            pd.DataFrame: DataFrame con una nueva columna "Ingresos Ajustados".
        """
        # Crear un diccionario con la inflación anual
        inflacion_dict = self.df_inflacion_anual.set_index("Año")["Inflación Anual (%)"].to_dict()
        
        # Obtener la inflación del año base
        inflacion_base = inflacion_dict[self.anio_base]
        
        # Calcular los ingresos ajustados para cada trimestre
        self.df_ingresos["Ingresos Ajustados"] = self.df_ingresos.apply(
            lambda row: row["Ingresos (miles de pesos)"] * (inflacion_base / inflacion_dict[row["Año"]]),
            axis=1
        )
        
        # Agrupar por año y calcular el total ajustado
        df_anual = self.df_ingresos.groupby("Año", as_index=False).agg({
            "Ingresos Ajustados": "sum"
        })
        
        return df_anual
    
    def _graficar_ingresos(self, anio_inicio=2014, anio_fin=2023):
        """
        Grafica los ingresos ajustados por inflación para los años especificados.
        
        Args:
            anio_inicio (int): Año inicial del rango a graficar.
            anio_fin (int): Año final del rango a graficar.
        """
        # Filtrar los datos por rango de años
        df_filtrado = self.df_ajustado[
            (self.df_ajustado["Año"] >= anio_inicio) & 
            (self.df_ajustado["Año"] <= anio_fin)
        ]
        
        if not df_filtrado.empty:
            # Crear gráfico de líneas
            fig = px.line(
                df_filtrado,
                x="Año",                   # Eje x: Año
                y="Ingresos Ajustados",    # Eje y: Ingresos Ajustados
                title=f"Evolución de los Ingresos Ajustados por Inflación Anual ({anio_inicio}-{anio_fin}) (Base {self.anio_base})",
                labels={
                    "Ingresos Ajustados": "Ingresos Ajustados (miles de pesos)",
                    "Año": "Año"
                },
                markers=True
            )
            fig.update_traces(mode="lines+markers")  # Mostrar puntos junto con las líneas
            fig.show()
        else:
            print("No hay datos disponibles para graficar en el rango especificado.")
    
    def display(self, anio_inicio=2014, anio_fin=2023):
        """
        Muestra el gráfico interactivo con los ingresos ajustados por inflación anual.
        
        Args:
            anio_inicio (int): Año inicial del rango a graficar.
            anio_fin (int): Año final del rango a graficar.
        """
        self._graficar_ingresos(anio_inicio, anio_fin)
        

class TotalAccesosPorRango:
    def __init__(self, df):
        """
        Inicializa la clase con el DataFrame de totales de accesos por rango.

        Args:
            df (pd.DataFrame): DataFrame con columnas Año, Trimestre y rangos de velocidades.
        """
        self.df = df

        # Crear widgets de selección
        self.año_widget = widgets.Dropdown(
            options=self.df["Año"].unique(),
            description="Año:"
        )
        self.trimestre_widget = widgets.Dropdown(
            options=self.df["Trimestre"].unique(),
            description="Trimestre:"
        )

        # Conexión de widgets con la función de graficado
        self.output = interactive_output(
            self._graficar_barras,
            {"año": self.año_widget, "trimestre": self.trimestre_widget}
        )

    def _graficar_barras(self, año, trimestre):
        """
        Grafica un diagrama de barras para un año y trimestre específicos.

        Args:
            año (int): Año seleccionado.
            trimestre (int): Trimestre seleccionado.
        """
        # Filtrar el DataFrame para el año y trimestre seleccionados
        df_filtrado = self.df[(self.df["Año"] == año) & (self.df["Trimestre"] == trimestre)]

        if not df_filtrado.empty:
            # Seleccionar columnas de rangos de velocidad
            categorias = [
                "Hasta 512 kbps",
                "Entre 512 Kbps y 1 Mbps",
                "Entre 1 Mbps y 6 Mbps",
                "Entre 6 Mbps y 10 Mbps",
                "Entre 10 Mbps y 20 Mbps",
                "Entre 20 Mbps y 30 Mbps",
                "Más de 30 Mbps",
                "OTROS"
            ]
            valores = df_filtrado.iloc[0][categorias]

            # Asignar colores personalizados
            colores = {
                "Hasta 512 kbps": "blue",
                "Entre 512 Kbps y 1 Mbps": "green",
                "Entre 1 Mbps y 6 Mbps": "orange",
                "Entre 6 Mbps y 10 Mbps": "purple",
                "Entre 10 Mbps y 20 Mbps": "red",
                "Entre 20 Mbps y 30 Mbps": "brown",
                "Más de 30 Mbps": "pink",
                "OTROS": "gray"
            }

            # Crear gráfico de barras
            fig = px.bar(
                x=categorias,
                y=valores,
                labels={"x": "Rango de Velocidad", "y": "Cantidad de Accesos"},
                title=f"Distribución de Accesos por Velocidad ({año} - Trimestre {trimestre})",
                text=valores
            )
            # Asignar colores a cada barra
            fig.update_traces(marker_color=[colores[cat] for cat in categorias], textposition="outside")
            fig.update_layout(xaxis_title="Rango de Velocidad", yaxis_title="Cantidad de Accesos")
            fig.show()
        else:
            print("No hay datos disponibles para el año y trimestre seleccionados.")

    def display(self):
        """
        Muestra los widgets y el gráfico interactivo.
        """
        display(widgets.VBox([widgets.HBox([self.año_widget, self.trimestre_widget]), self.output]))


class GraficoAccesosPorTecnologia:
    def __init__(self, df):
        """
        Inicializa la clase con el DataFrame de totales de accesos por tecnología.

        Args:
            df (pd.DataFrame): DataFrame con columnas Año, Trimestre y tecnologías de acceso.
        """
        self.df = df

        # Crear widgets de selección
        self.año_widget = widgets.Dropdown(
            options=self.df["Año"].unique(),
            description="Año:"
        )
        self.trimestre_widget = widgets.Dropdown(
            options=self.df["Trimestre"].unique(),
            description="Trimestre:"
        )

        # Conexión de widgets con la función de graficado
        self.output = interactive_output(
            self._graficar_barras,
            {"año": self.año_widget, "trimestre": self.trimestre_widget}
        )

    def _graficar_barras(self, año, trimestre):
        """
        Grafica un diagrama de barras horizontal para un año y trimestre específicos.

        Args:
            año (int): Año seleccionado.
            trimestre (int): Trimestre seleccionado.
        """
        # Filtrar el DataFrame para el año y trimestre seleccionados
        df_filtrado = self.df[(self.df["Año"] == año) & (self.df["Trimestre"] == trimestre)]

        if not df_filtrado.empty:
            # Seleccionar columnas de tecnologías de acceso
            tecnologias = ["ADSL", "Cablemodem", "Fibra óptica", "Wireless", "Otros"]
            valores = df_filtrado.iloc[0][tecnologias]

            # Asignar colores personalizados
            colores = {
                "ADSL": "blue",
                "Cablemodem": "green",
                "Fibra óptica": "orange",
                "Wireless": "purple",
                "Otros": "red"
            }

            # Crear gráfico de barras horizontal
            fig = px.bar(
                x=valores,
                y=tecnologias,
                orientation="h",
                labels={"x": "Cantidad de Accesos", "y": "Tecnología"},
                title=f"Distribución de Accesos por Tecnología ({año} - Trimestre {trimestre})",
                text=valores
            )

            # Aplicar colores personalizados a las barras
            fig.update_traces(marker_color=[colores[tec] for tec in tecnologias], textposition="outside")
            fig.update_layout(xaxis_title="Cantidad de Accesos", yaxis_title="Tecnología")
            fig.show()
        else:
            print("No hay datos disponibles para el año y trimestre seleccionados.")

    def display(self):
        """
        Muestra los widgets y el gráfico interactivo.
        """
        display(widgets.VBox([widgets.HBox([self.año_widget, self.trimestre_widget]), self.output]))


class GraficoPenetracionHogares:
    def __init__(self, df):
        """
        Inicializa la clase con el DataFrame de penetración de hogares.

        Args:
            df (pd.DataFrame): DataFrame con columnas Año, Trimestre, Provincia, Accesos por cada 100 hogares.
        """
        self.df = df

        # Crear widgets de selección con valores predeterminados
        self.año_widget = widgets.Dropdown(
            options=self.df["Año"].unique(),
            value=2022,  # Año por defecto
            description="Año:"
        )
        self.provincia_widget = widgets.Dropdown(
            options=self.df["Provincia"].unique(),
            value="Córdoba",  # Provincia por defecto
            description="Provincia:"
        )

        # Conexión de widgets con la función de graficado
        self.output = interactive_output(
            self._graficar_penetracion,
            {"año": self.año_widget, "provincia": self.provincia_widget}
        )

    def _graficar_penetracion(self, año, provincia):
        """
        Grafica un diagrama de líneas para un año y provincia específicos.

        Args:
            año (int): Año seleccionado.
            provincia (str): Provincia seleccionada.
        """
        # Filtrar el DataFrame para el año y la provincia seleccionados
        df_filtrado = self.df[(self.df["Año"] == año) & (self.df["Provincia"] == provincia)]

        if not df_filtrado.empty:
            # Ordenar los datos por trimestre de menor a mayor
            df_filtrado = df_filtrado.sort_values(by="Trimestre")

            # Crear gráfico de líneas
            fig = px.line(
                df_filtrado,
                x="Trimestre",                     # Eje x: Trimestre
                y="Accesos por cada 100 hogares",  # Eje y: Accesos por cada 100 hogares
                title=f"Penetración de Accesos por Hogares en {provincia} ({año})",
                labels={
                    "Trimestre": "Trimestre",
                    "Accesos por cada 100 hogares": "Accesos por cada 100 Hogares"
                },
                markers=True
            )
            fig.update_traces(mode="lines+markers", line=dict(width=2))
            fig.update_xaxes(type="category")  # Asegurar categorías en el eje x
            fig.show()
        else:
            print("No hay datos disponibles para el año y provincia seleccionados.")

    def display(self):
        """
        Muestra los widgets y el gráfico interactivo.
        """
        display(widgets.VBox([widgets.HBox([self.año_widget, self.provincia_widget]), self.output]))



class GraficoVelocidadPromedio:
    def __init__(self, df):
        """
        Inicializa la clase con el DataFrame de velocidad promedio por provincia.

        Args:
            df (pd.DataFrame): DataFrame con columnas Año, Trimestre, Provincia, Mbps (Media de bajada).
        """
        self.df = df

        # Crear widgets de selección con valores predeterminados
        self.año_widget = widgets.Dropdown(
            options=self.df["Año"].unique(),
            value=2022,  # Año por defecto
            description="Año:"
        )
        self.provincia_widget = widgets.Dropdown(
            options=self.df["Provincia"].unique(),
            value="Capital Federal",  # Provincia por defecto
            description="Provincia:"
        )

        # Conexión de widgets con la función de graficado
        self.output = interactive_output(
            self._graficar_velocidad,
            {"año": self.año_widget, "provincia": self.provincia_widget}
        )

    def _graficar_velocidad(self, año, provincia):
        """
        Grafica un diagrama de líneas para un año y provincia específicos.

        Args:
            año (int): Año seleccionado.
            provincia (str): Provincia seleccionada.
        """
        # Filtrar el DataFrame para el año y la provincia seleccionados
        df_filtrado = self.df[(self.df["Año"] == año) & (self.df["Provincia"] == provincia)]

        if not df_filtrado.empty:
            # Ordenar los datos por trimestre de menor a mayor
            df_filtrado = df_filtrado.sort_values(by="Trimestre")

            # Crear gráfico de líneas
            fig = px.line(
                df_filtrado,
                x="Trimestre",                 # Eje x: Trimestre
                y="Mbps (Media de bajada)",    # Eje y: Mbps (Media de bajada)
                title=f"Velocidad Promedio (Mbps) en {provincia} ({año})",
                labels={
                    "Trimestre": "Trimestre",
                    "Mbps (Media de bajada)": "Velocidad Promedio (Mbps)"
                },
                markers=True
            )
            fig.update_traces(mode="lines+markers", line=dict(width=2))
            fig.update_xaxes(type="category")  # Asegurar categorías en el eje x
            fig.show()
        else:
            print("No hay datos disponibles para el año y provincia seleccionados.")

    def display(self):
        """
        Muestra los widgets y el gráfico interactivo.
        """
        display(widgets.VBox([widgets.HBox([self.año_widget, self.provincia_widget]), self.output]))