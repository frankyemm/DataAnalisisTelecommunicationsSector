import pandas as pd

# Crear el dataset de inflación anual desde 2014 hasta 2024
data_inflacion_anual = {
    "Año": [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    "Inflación Anual (%)": [38.5, 26.9, 40.0, 24.8, 47.6, 53.5, 36.1, 50.9, 94.8, 120.0]
}

# Convertir a DataFrame
df_inflacion_anual = pd.DataFrame(data_inflacion_anual)



# Guardar en un archivo CSV
df_inflacion_anual.to_csv("Data_cleaned/Inflacion_Anual_Argentina_2014_2024.csv", index=False)

