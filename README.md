# Proyecto: Análisis del Sector de Telecomunicaciones en Argentina

## Descripción General

Este proyecto tiene como objetivo analizar el comportamiento del sector de telecomunicaciones en Argentina utilizando datos relevantes sobre velocidad de internet, penetración de hogares conectados, tecnologías utilizadas y métricas financieras ajustadas por inflación. El análisis incluye:
- Exploración de datos (EDA) y visualización interactiva.
- Creación de KPIs clave para evaluar el crecimiento y las oportunidades en el mercado.
- Generación de insights basados en datos para orientar decisiones estratégicas.

---

## Estructura del Proyecto

### Carpetas Principales

#### 1. `Datasets`
- Contiene los datasets originales extraídos del archivo Excel **`Internet.xlsx`**.
- Los datos no han sido limpiados.
- Datasets incluidos:
  - **Velocidad % por prov**
  - **Penetración-hogares**
  - **Totales Accesos Por Tecnología**
  - **Totales Accesos por rango**
  - **Accesos por rangos**
  - **Ingresos**

#### 2. `Data_cleaned`
- Contiene los datasets limpios listos para el análisis.
- Cada archivo es una versión procesada de los originales en `Datasets`.
- Estructura y nombres iguales a los de `Datasets`.

---

## Archivos Principales

### 1. `requirements.txt`
- Contiene las dependencias necesarias para ejecutar el proyecto.
- Instalación:
  ```bash
  pip install -r requirements.txt
### 2. `graficos.py`
- Proporciona funciones para crear gráficos interactivos relacionados con:
    - Distribución de accesos por rangos.
    - Distribución de accesos por tecnologías.
    - Evolución de penetración de hogares conectados.
    - Velocidad promedio de internet por provincia.
- Utiliza `plotly` para visualización y ipywidgets para interactividad.
- Ejemplo de uso:
  ```python
  from graficos import GraficoAccesosPorTecnologia
  grafico = GraficoAccesosPorTecnologia(df_tecnologia)
  grafico.display()
### 3. `inflacion.py`
- Funcionalidad:
  - Generación de un dataset con tasas de inflación anual desde 2014 hasta 2024.
  - Ajuste de ingresos trimestrales por inflación basado en un año base.
- Ejemplo de uso:
  ```python
  from inflacion import ajustar_ingresos
  ingresos_ajustados = ajustar_ingresos(df_ingresos, df_inflacion)
### 4. `KPIs.py`
- Calcula y grafica 3 KPIs clave:
  - **Penetración de accesos por hogares.**
  - **Velocidad promedio por provincia.**
  - **Cobertura de fibra óptica por trimestre.**
- Los KPIs incluyen filtros interactivos y gráficos detallados.
- Ejemplo de uso
  ```python
  from KPIs import KPIAnalyzer
  kpi_analyzer = KPIAnalyzer(df_penetracion, df_velocidad, df_fibra)
  kpi_analyzer.display()
### 5. `EDA_Analysis_Telecommunications_Sector.ipynb`
- Notebook interactivo que:
  - Realiza el análisis exploratorio de los datos (EDA).
  - Incluye visualizaciones y descripciones detalladas.
  - Integra las métricas y gráficos generados por los módulos.
---
## Resultados y Análisis de KPIs
### **KPI 1: Penetración de accesos por hogares**
- **Fórmula**:  

  $KPI = \left(\frac{\text{Nuevo acceso} - \text{Acceso actual}}{\text{Acceso actual}}\right) \times 100$

- **Variables necesarias**:
  - *Acceso actual*: Accesos por cada 100 hogares en el trimestre actual.
  - *Nuevo acceso*: Proyección del número de accesos por cada 100 hogares tras el incremento del 2%.
- **Descripción**: Evalúa el crecimiento porcentual de accesos en hogares durante los trimestres 3 y 4 del 2023.
- **Resultados**:
  - Crecimiento positivo en provincias como Buenos Aires y Córdoba.
  - Provincias rurales muestran menor penetración.
- **Recomendaciones**:
  - Invertir en áreas rurales para reducir la brecha digital.
  - Promover políticas públicas que incentiven el acceso.
### **KPI 2: Velocidad promedio de internet**
- **Fórmula**:  

  $KPI = \left(\frac{\text{Nueva velocidad promedio} - \text{Velocidad promedio actual}}{\text{Velocidad promedio actual}}\right) \times 100$

- **Variables necesarias**:
  - *Velocidad promedio actual*: Media de las velocidades actuales por provincia (Mbps).
  - *Nueva velocidad promedio*: Proyección de la velocidad promedio tras el incremento del 2%.
- **Descripción**: Analiza el incremento en Mbps promedio en las provincias entre los trimestres 3 y 4 del 2023.
- **Resultados**:
  - Capital Federal lidera con velocidades superiores a 180 Mbps.
  - Regiones menos urbanizadas presentan velocidades más bajas.
- **Recomendaciones**:
  - Expandir la infraestructura de fibra óptica en regiones con velocidades bajas.
  - Incentivar a las ISPs a mantener estándares elevados de calidad.
### **KPI 3: Cobertura de fibra óptica**
- **Fórmula**:

  $KPI = \left(\frac{\text{Total Accesos proyectados} - \text{Total Accesos actuales}}{\text{Total Accesos actuales}}\right) \times 100$
  
- **Variables necesarias**:
  - *Accesos actuales*: Total de Accesos por tecnologías (Fibra Óptica) en el trimestre actual.
  - *Ingresos proyectados*: Proyección de Accesos por tecnologías (Fibra Óptica) con un incremento del 1.5%.
- **Descripción**: Mide el crecimiento de accesos por fibra óptica en los trimestres 3 y 4 del 2023.
- **Resultados**:
  - Incrementos significativos en provincias como Mendoza y Córdoba.
  - ADSL y tecnologías obsoletas aún tienen presencia considerable.
- **Recomendaciones**:
  - Enfocarse en la transición de ADSL a fibra óptica.
  - Expandir la cobertura en zonas suburbanas y rurales.
---
## Tecnologías Utilizadas
- **Pandas**: Manipulación de datos.
- **Plotly**: Visualizaciones interactivas.
- **Ipywidgets**: Interactividad en Jupyter Notebook.
- **Python**: Lenguaje principal del proyecto.
- **Excel**: Origen de los datos.
---
## Ejecución del Proyecto
### 1. Configuración Inicial
- Instalar dependencias:
    ```bash
    pip install -r requirements.txt
- Asegurarse de que las carpetas Datasets y Data_cleaned contengan los archivos correspondientes.
### 2. Exploración de Datos
- Ejecutar el archivo EDA_Analysis_Telecommunications_Sector.ipynb para obtener un análisis inicial de los datos.
- Este notebook incluye:
  - Gráficos descriptivos.
  - Estadísticas clave.
  - Identificación de tendencias.
### 3. Generación de Visualizaciones
- Usar las clases en graficos.py para generar gráficos interactivos.
- Por ejemplo, para graficar la distribución de accesos por tecnología:
    ```python
    from graficos import GraficoAccesosPorTecnologia
    grafico = GraficoAccesosPorTecnologia(df_tecnologia)
    grafico.display()
### 4. Cálculo de KPIs
- Importar y usar las clases de KPIs.py para analizar los indicadores clave de rendimiento.
- Ejemplo:
    ```python
    from KPIs import KPIAnalyzer
    kpi_analyzer = KPIAnalyzer(df_penetracion, df_velocidad, df_fibra)
    kpi_analyzer.display()
### 5. Ajuste por Inflación
- Utilizar el módulo inflacion.py para calcular ingresos ajustados.
- Ejemplo:
    ```python
    from inflacion import ajustar_ingresos
    ingresos_ajustados = ajustar_ingresos(df_ingresos, df_inflacion)
---
## Conclusiones Generales
1. **Transición a Tecnologías Modernas**:
    - Predominio de fibra óptica y cablemódem.
    - Necesidad de acelerar la sustitución de tecnologías obsoletas.
2. **Crecimiento en Conectividad**:
    - Provincias urbanas lideran en penetración.
    - Brechas digitales significativas en áreas rurales.
3. **Velocidades en Ascenso**:
    - Tendencia positiva en regiones clave.
    - Disparidades notables entre provincias.
4. **Ingresos Estables**:
    - Ajustados por inflación, los ingresos muestran sostenibilidad.
---
## Recomendaciones Estratégicas
1. Invertir en Infraestructura:
    - Expandir fibra óptica a zonas rurales.
    - Garantizar la estabilidad de velocidades altas.
2. **Reducir la Brecha Digital**:
    - Promover subsidios para hogares no conectados.
    - Incentivar acceso en comunidades vulnerables.
3. **Fortalecer Políticas de Calidad**:
    - Regular estándares mínimos para ISPs.
    - Monitorizar mejoras en tecnologías existentes.
4. **Aprovechar el Potencial del Mercado**:
    - Explorar oportunidades en regiones en desarrollo.
    - Usar datos de KPIs para ajustar estrategias de inversión.
---
## Próximos Pasos
1. **Ampliación del Análisis**:
    - Incluir predicciones de tendencias futuras mediante modelos de Machine Learning.
    - Identificar nuevas métricas basadas en la demanda de mercado.
2. **Optimización de Infraestructura**:
    - Usar los insights obtenidos para diseñar estrategias de inversión en infraestructura tecnológica.
3. **Expansión Regional**:
    - Focalizar esfuerzos en regiones con bajo crecimiento y alto potencial.
---
## Contribuciones
Para sugerencias o colaboraciones, por favor contacta a través de los canales disponibles en este repositorio.

---
## Licencia
Este proyecto está licenciado bajo la [Licencia MIT](LICENSE). Puedes usar, modificar y distribuir el código con los créditos correspondientes.

---
## Créditos
Este proyecto fue desarrollado como parte del análisis del sector de telecomunicaciones en Argentina, utilizando herramientas de análisis de datos avanzadas para generar insights estratégicos.