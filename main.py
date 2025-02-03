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



def clusterizar_deforestacion(df):
    """Realiza un análisis de clúster sobre las superficies deforestadas.

    Args:
        df (pd.DataFrame): DataFrame con columnas 'Latitud', 'Longitud', 'Superficie_Deforestada'.
    """
    st.write("### Análisis de Clúster de Deforestación")
    df['cluster'] = np.digitize(df['Superficie_Deforestada'], bins=np.histogram_bin_edges(df['Superficie_Deforestada'], bins=3))
    fig, ax = plt.subplots()
    scatter = ax.scatter(df['Longitud'], df['Latitud'], c=df['cluster'], cmap='viridis')
    plt.colorbar(scatter)
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

if __name__ == "__main__":
    main()
