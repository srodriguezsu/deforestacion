import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from scipy.interpolate import griddata
from shapely.geometry import Point

def cargar_datos():
    """Carga datos desde la URL fija del archivo de deforestación.

    Returns:
        pd.DataFrame: DataFrame con los datos cargados e interpolados.
    """
    url = "https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/refs/heads/main/archivos-datos/aplicaciones/deforestacion.csv"
    df = pd.read_csv(url)
    return df.interpolate(method='linear')

def mostrar_estadisticas(df):
    """Muestra estadísticas generales del dataset."""
    st.write("### Estadísticas Generales")
    st.write(df.describe())

def mostrar_mapa_deforestacion(df):
    """Genera un mapa con las zonas de deforestación usando imágenes satelitales.

    Args:
        df (pd.DataFrame): DataFrame con las columnas 'Latitud', 'Longitud', 'Superficie_Deforestada'.
    """
    st.write("### Mapa de Zonas Deforestadas")
    route = "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"

    world = gpd.read_file(route)
    df['geometry'] = df.apply(lambda row: Point(row['Longitud'], row['Latitud']), axis=1)
    gdf = gpd.GeoDataFrame(df, geometry='geometry')
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

def main():
    """Función principal para ejecutar la aplicación de análisis de deforestación."""
    st.title("Análisis de Deforestación")
    df = cargar_datos()
    if df is not None:
        mostrar_estadisticas(df)
        mostrar_mapa_deforestacion(df)
        clusterizar_deforestacion(df)
        grafico_torta_vegetacion(df)

if __name__ == "__main__":
    main()
