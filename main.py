import geopandas as gpd
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from shapely.geometry import Point

def load_data(file=None, url=None):
    """Carga los datos desde un archivo o una URL."""
    if file is not None:
        return pd.read_csv(file)
    elif url is not None:
        return pd.read_csv(url)
    else:
        return None
def analizar_deforestacion(df):
    """Realiza un análisis básico de deforestación a partir de un DataFrame con las columnas proporcionadas."""
    
    # Convertir las columnas numéricas a float si es necesario
    df['Superficie_Deforestada'] = df['Superficie_Deforestada'].astype(float)
    df['Tasa_Deforestacion'] = df['Tasa_Deforestacion'].astype(float)
    df['Altitud'] = df['Altitud'].astype(float)
    df['Pendiente'] = df['Pendiente'].astype(float)
    df['Distancia_Carretera'] = df['Distancia_Carretera'].astype(float)
    df['Precipitacion'] = df['Precipitacion'].astype(float)
    df['Temperatura'] = df['Temperatura'].astype(float)

    st.write("# Análisis de datos")
    
    # Analizar superficie deforestada total
    superficie_deforestada_total = df['Superficie_Deforestada'].sum()
    st.write(f"Superficie deforestada total: {superficie_deforestada_total:.2f} ha")
    
    # Analizar la tasa de deforestación promedio
    tasa_deforestacion_promedio = df['Tasa_Deforestacion'].mean()
    st.write(f"Tasa de deforestación promedio: {tasa_deforestacion_promedio:.4f}")
    
    # Tendencia temporal de la superficie deforestada
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df.set_index('Fecha', inplace=True)
    
    superficie_deforestada_anual = df.resample('Y')['Superficie_Deforestada'].sum()
    
    st.write("Superficie deforestada anual:")
    st.write(superficie_deforestada_anual)
    
    # Gráfico de la superficie deforestada anual
    fig, ax = plt.subplots(figsize=(10, 5))
    superficie_deforestada_anual.plot(kind='line', ax=ax, marker='o', color='tab:red')
    ax.set_title('Superficie deforestada anual')
    ax.set_xlabel('Año')
    ax.set_ylabel('Superficie deforestada (ha)')
    st.pyplot(fig)

    # Relación de variables geográficas y climáticas con la deforestación
    st.write("Correlaciones entre las variables y la superficie deforestada:")
    correlaciones = df[['Latitud', 'Longitud', 'Altitud', 'Pendiente', 'Distancia_Carretera', 'Precipitacion', 'Temperatura', 'Superficie_Deforestada']].corr()
    st.write(correlaciones)

    # Gráfico de correlación
    fig, ax = plt.subplots(figsize=(10, 8))
    cax = ax.matshow(correlaciones, cmap='coolwarm')
    fig.colorbar(cax)
    ax.set_xticks(np.arange(len(correlaciones.columns)))
    ax.set_yticks(np.arange(len(correlaciones.columns)))
    ax.set_xticklabels(correlaciones.columns, rotation=90)
    ax.set_yticklabels(correlaciones.columns)
    st.pyplot(fig)

    # Histograma de la temperatura y deforestación
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(df['Temperatura'], df['Superficie_Deforestada'], color='tab:blue')
    ax.set_title('Temperatura vs Superficie deforestada')
    ax.set_xlabel('Temperatura (°C)')
    ax.set_ylabel('Superficie deforestada (ha)')
    st.pyplot(fig)
        

def cargar_mapa_mundo():
    """Carga el mapa mundial utilizando GeoPandas."""
    ruta_0 = "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"
    return gpd.read_file(ruta_0)


def crear_geodataframe(df):
    """Convierte un DataFrame con columnas de latitud y longitud en un GeoDataFrame."""
    # Asegúrate de que latitud y longitud sean numéricas
    df['Latitud'] = pd.to_numeric(df['Latitud'], errors='coerce')
    df['Longitud'] = pd.to_numeric(df['Longitud'], errors='coerce')
    
    # Crear una nueva columna de geometría como puntos (lat, long)
    geometry = [Point(xy) for xy in zip(df['Longitud'], df['Latitud'])]
    
    # Crear un GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry=geometry)
    gdf.set_crs(epsg=4326, inplace=True)  # Usar el sistema de referencia espacial WGS 84
    return gdf


def graficar_zonas_deforestadas(gdf, variable, mapa_mundo):
    """Grafica el mapa de zonas deforestadas según una variable (tipo de vegetación, altitud, precipitación)."""
    # Primero, asegurarnos que la variable existe en el DataFrame
    st.write(f"# Grafio de zonas deforestadas segun {variable}")
    if variable not in gdf.columns:
        st.warning(f"La variable {variable} no se encuentra en los datos.")
        return

    # Crear una figura y un eje para el gráfico
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Graficar el mapa mundial
    mapa_mundo.plot(ax=ax, color='lightgrey', edgecolor='black')

    # Graficar las zonas deforestadas según la variable seleccionada
    gdf.plot(ax=ax, column=variable, legend=True, cmap='coolwarm', markersize=5, alpha=0.7)

    # Títulos y etiquetas
    ax.set_title(f"Zonas deforestadas por {variable}", fontsize=16)
    ax.set_xlabel('Longitud')
    ax.set_ylabel('Latitud')

    # Mostrar el gráfico
    st.pyplot(fig)


def main():
    st.title('Aplicación de Deforestación')

    # Opción para cargar datos desde archivo o URL
    option = st.radio("Selecciona cómo cargar los datos", ("Subir archivo", "Usar URL"))

    data = None
    if option == "Subir archivo":
        uploaded_file = st.file_uploader("Elige un archivo CSV", type=["csv"])
        if uploaded_file is not None:
            data = load_data(file=uploaded_file)
    elif option == "Usar URL":
        url = st.text_input("Introduce la URL del archivo CSV")
        if url:
            data = load_data(url=url)

    if data is not None:
        st.write("Datos cargados exitosamente:")
        data = data.interpolate(method='linear')
        
        st.write(data)
        analizar_deforestacion(data)

                # Crear un GeoDataFrame a partir de los datos
        gdf = crear_geodataframe(data)

        # Cargar el mapa mundial
        mapa_mundo = cargar_mapa_mundo()
        
        graficar_zonas_deforestadas(gdf, 'Tipo_Vegetacion', mapa_mundo)        
        graficar_zonas_deforestadas(gdf, 'Altitud', mapa_mundo)        
        graficar_zonas_deforestadas(gdf, 'Precipitacion', mapa_mundo)        
        st.write("Selecciona hasta 4 variables para filtrar los datos y visualizar el mapa.")
        
        variables = ['Latitud', 'Longitud', 'Tipo_Vegetacion', 'Altitud', 'Precipitacion']

        # Crear un diccionario para almacenar los valores seleccionados
        variables_seleccionadas = {}

        for variable in variables:
            if variable in gdf.columns:
                # Si la variable es numérica, ofrecer un rango
                if pd.api.types.is_numeric_dtype(gdf[variable]):
                    min_val = gdf[variable].min()
                    max_val = gdf[variable].max()
                    st.write(f"Selecciona un rango para {variable}.")
                    valores = st.slider(f"{variable}", min_val, max_val, (min_val, max_val))
                    variables_seleccionadas[variable] = valores
                # Si la variable es categórica, ofrecer un desplegable
                else:
                    opciones = gdf[variable].unique()
                    seleccionados = st.multiselect(f"Selecciona las categorías para {variable}.", opciones, default=opciones)
                    variables_seleccionadas[variable] = seleccionados

        # Filtrar y graficar el mapa según las variables seleccionadas
        if variables_seleccionadas:
            graficar_zonas_deforestadas(gdf, variables_seleccionadas, mapa_mundo)
        else:
            st.warning("No se han seleccionado variables para filtrar.")

        
        
    else:
        st.warning("Por favor, carga un archivo o ingresa una URL válida.")


if __name__ == "__main__":
    main()
