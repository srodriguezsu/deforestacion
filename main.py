import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point

def cargar_datos():
    """Carga datos desde la URL fija del archivo de deforestación."""
    url = "https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/refs/heads/main/archivos-datos/aplicaciones/deforestacion.csv"
    df = pd.read_csv(url)
    return df.interpolate(method='linear')

def grafico_torta_vegetacion(df):
    """Genera un gráfico de torta según el tipo de vegetación.

    Args:
        df (pd.DataFrame): DataFrame con columna 'Tipo_Vegetacion'.
    """
    st.write("### Distribución por Tipo de Vegetación")
    tipo_veg = df['Tipo_Vegetacion'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(tipo_veg, labels=tipo_veg.index, autopct='%1.1f%%', startangle=90)
    st.pyplot(fig)


def mostrar_estadisticas(df):
    """Muestra estadísticas generales del dataset."""
    st.write("### Estadísticas Generales")
    st.write(df.describe())

def mostrar_mapa_deforestacion(df, variables_seleccionadas, rango_latitud, rango_longitud, rango_altitud, rango_precipitacion):
    """Genera un mapa con las zonas de deforestación según las variables seleccionadas por el usuario."""
    st.write("### Mapa de Zonas Deforestadas Filtrado")
    
    # Filtrar el dataframe según las selecciones del usuario
    if variables_seleccionadas:
        for var in variables_seleccionadas:
            if var == 'Latitud':
                df = df[(df['Latitud'] >= rango_latitud[0]) & (df['Latitud'] <= rango_latitud[1])]
            if var == 'Longitud':
                df = df[(df['Longitud'] >= rango_longitud[0]) & (df['Longitud'] <= rango_longitud[1])]
            if var == 'Altitud':
                df = df[(df['Altitud'] >= rango_altitud[0]) & (df['Altitud'] <= rango_altitud[1])]
            if var == 'Precipitacion':
                df = df[(df['Precipitacion'] >= rango_precipitacion[0]) & (df['Precipitacion'] <= rango_precipitacion[1])]
    
    # Generar la geometría para GeoDataFrame
    df['geometry'] = df.apply(lambda row: Point(row['Longitud'], row['Latitud']), axis=1)
    gdf = gpd.GeoDataFrame(df, geometry='geometry')

    # Crear el mapa
    route = "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"
    world = gpd.read_file(route)
    fig, ax = plt.subplots(figsize=(10, 6))
    world.plot(ax=ax, color='lightgray')
    gdf.plot(ax=ax, column='Superficie_Deforestada', legend=True, cmap='Reds', markersize=5)
    st.pyplot(fig)


def mostrar_mapas_deforestacion(df):
    """Genera mapas de las zonas deforestadas basados en el tipo de vegetación, 
    altitud y precipitación.
    
    Args:
        df (pd.DataFrame): DataFrame 
    Returns:
        None: Muestra tres mapas en Streamlit, uno por cada variable (Tipo de Vegetación, Altitud, Precipitación).
    """
    
    # Convertir las coordenadas en puntos geográficos y crear un GeoDataFrame
    df['geometry'] = df.apply(lambda row: Point(row['Longitud'], row['Latitud']), axis=1)
    gdf = gpd.GeoDataFrame(df, geometry='geometry')
    
    # Descargar un mapa base del mundo para mostrar las zonas de deforestación
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    
    # Filtrar el mapa mundial para obtener solo América del Sur (opcional)
    # world = world[world['continent'] == 'South America']
    
    # Plot mapa de zonas deforestadas por Tipo de Vegetación
    st.write("### Mapa de Zonas Deforestadas por Tipo de Vegetación")
    fig, ax = plt.subplots(figsize=(10, 6))
    world.plot(ax=ax, color='lightgray')
    gdf.plot(ax=ax, column='Tipo_Vegetacion', legend=True, cmap='Set3', markersize=10, legend_kwds={'bbox_to_anchor': (1, 1)})
    ax.set_title("Zonas Deforestadas por Tipo de Vegetación")
    st.pyplot(fig)

    # Plot mapa de zonas deforestadas por Altitud
    st.write("### Mapa de Zonas Deforestadas por Altitud")
    fig, ax = plt.subplots(figsize=(10, 6))
    world.plot(ax=ax, color='lightgray')
    gdf.plot(ax=ax, column='Altitud', legend=True, cmap='YlGnBu', markersize=10, legend_kwds={'bbox_to_anchor': (1, 1)})
    ax.set_title("Zonas Deforestadas por Altitud")
    st.pyplot(fig)

    # Plot mapa de zonas deforestadas por Precipitación
    st.write("### Mapa de Zonas Deforestadas por Precipitación")
    fig, ax = plt.subplots(figsize=(10, 6))
    world.plot(ax=ax, color='lightgray')
    gdf.plot(ax=ax, column='Precipitacion', legend=True, cmap='Blues', markersize=10, legend_kwds={'bbox_to_anchor': (1, 1)})
    ax.set_title("Zonas Deforestadas por Precipitación")
    st.pyplot(fig)


def clusterizar_deforestacion(df):
    """Realiza un análisis de clúster sobre las superficies deforestadas, 
    asignando un número de clúster a cada punto de datos según la superficie deforestada.
    
    Este análisis ayuda a identificar patrones o agrupaciones en los datos de deforestación 
    según el tamaño de la superficie deforestada. Se utiliza la técnica de discretización de 
    la superficie deforestada en 3 grupos para categorizar los puntos en diferentes clústeres.
    
    Args:
        df (pd.DataFrame): DataFrame que contiene las siguientes columnas:
            - 'Latitud': Coordenada de latitud de la ubicación.
            - 'Longitud': Coordenada de longitud de la ubicación.
            - 'Superficie_Deforestada': Valor que representa la superficie deforestada en esa ubicación.
    
    Returns:
        None: La función no retorna valores, pero muestra un gráfico de dispersión con 
              los puntos de datos agrupados por clúster.
    """
    # Muestra un título para la sección de análisis de clúster
    st.write("### Análisis de Clúster de Deforestación")
    
    # Crea los bins para dividir las superficies deforestadas en 3 grupos
    # `np.histogram_bin_edges` devuelve los límites de los bins, que luego usamos en `np.digitize` 
    # para asignar cada superficie a un clúster (1, 2, o 3).
    bins = np.histogram_bin_edges(df['Superficie_Deforestada'], bins=3)
    df['cluster'] = np.digitize(df['Superficie_Deforestada'], bins=bins)
    
    # Crear la figura para el gráfico de dispersión
    fig, ax = plt.subplots(figsize=(10, 6))  # Se define un tamaño adecuado para visualizar bien los puntos
    scatter = ax.scatter(df['Longitud'], df['Latitud'], c=df['cluster'], cmap='viridis', s=30)
    
    # Añadir una barra de color que muestra la relación entre el valor de clúster y el color
    plt.colorbar(scatter, label='Clúster de Superficie Deforestada')
    
    # Etiquetas y título
    ax.set_title("Distribución de Zonas Deforestadas por Clúster", fontsize=14)
    ax.set_xlabel("Longitud", fontsize=12)
    ax.set_ylabel("Latitud", fontsize=12)
    
    # Muestra el gráfico en Streamlit
    st.pyplot(fig)


def main():
    """Función principal para ejecutar la aplicación de análisis de deforestación."""
    st.title("Análisis de Deforestación")
    df = cargar_datos()
    
    if df is not None:
        mostrar_estadisticas(df)

        # Allow users to select variables for filtering
        st.write("### Filtrar Mapa por Variables")
        
        # Variables to filter by
        variables_seleccionadas = st.multiselect(
            "Selecciona hasta cuatro variables para filtrar el mapa",
            ['Latitud', 'Longitud', 'Altitud', 'Precipitacion', 'Tipo_Vegetacion']
        )
        
        # Rango de valores para cada variable
        if 'Latitud' in variables_seleccionadas:
            rango_latitud = st.slider('Rango de Latitud', min_value=float(df['Latitud'].min()), max_value=float(df['Latitud'].max()), value=(-5.0, 5.0))
        else:
            rango_latitud = (-90, 90)
        
        if 'Longitud' in variables_seleccionadas:
            rango_longitud = st.slider('Rango de Longitud', min_value=float(df['Longitud'].min()), max_value=float(df['Longitud'].max()), value=(-5.0, 5.0))
        else:
            rango_longitud = (-180, 180)

        if 'Altitud' in variables_seleccionadas:
            rango_altitud = st.slider('Rango de Altitud', min_value=int(df['Altitud'].min()), max_value=int(df['Altitud'].max()), value=(0, 1000))
        else:
            rango_altitud = (0, 5000)

        if 'Precipitacion' in variables_seleccionadas:
            rango_precipitacion = st.slider('Rango de Precipitación', min_value=int(df['Precipitacion'].min()), max_value=int(df['Precipitacion'].max()), value=(0, 200))
        else:
            rango_precipitacion = (0, 2000)

        # Display map based on selected filters
        mostrar_mapa_deforestacion(df, variables_seleccionadas, rango_latitud, rango_longitud, rango_altitud, rango_precipitacion)
        grafico_torta_vegetacion(df)
        clusterizar_deforestacion(df)
        mostrar_mapas_deforestacion(df)

if __name__ == "__main__":
    main()
