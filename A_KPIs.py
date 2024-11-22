import streamlit as st
import pandas as pd
from KPI_1 import KPIAnalyzerStreamlit

def render_kpi_analysis():
    
    # Cargar datos
    df_penetracion = pd.read_csv("Data_cleaned/Penetracion-hogares.csv")
    df_velocidad = pd.read_csv("Data_cleaned/Velocidad % por prov.csv")
    df_fibra = pd.read_csv("Data_cleaned/Totales Accesos Por Tecnología.csv")
    
    # Inicializar el analizador de KPIs
    kpi_app = KPIAnalyzerStreamlit(df_penetracion, df_velocidad, df_fibra)
    
    # Mostrar la visualización interactiva
    kpi_app.display()
