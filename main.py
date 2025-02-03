import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from scipy.interpolate import griddata


def cargar_datos():
    """Carga datos desde un archivo subido o una URL ingresada por el usuario.

    Returns:
        pd.DataFrame: DataFrame con los datos cargados e interpolados.
    """
    fuente = st.radio("Seleccione la fuente de datos", ("Archivo", "URL"))
    df = None

    df = (pd.read_csv(st.file_uploader("Suba un archivo CSV", type=["csv"])) 
          if fuente == "Archivo" else
          pd.read_csv(st.text_input("Ingrese la URL del archivo CSV")) if st.text_input("Ingrese la URL del archivo CSV") else None)
    
    return df.interpolate(method='linear') if df is not None else None


def mostrar_estadisticas(df):
    """Muestra estadísticas generales del dataset."""
    st.write("### Estadísticas Generales")
    st.write(df.describe())

def mostrar_mapa_deforestacion(df):
    """Genera un mapa con las zonas de deforestación.

    Args:
        df (pd.DataFrame): DataFrame con las columnas 'lat', 'lon', 'superficie_deforestada'.
    """
    st.write("### Mapa de Zonas Deforestadas")
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat))
    fig, ax = plt.subplots()
    gdf.plot(ax=ax, column='superficie_deforestada', legend=True, cmap='Reds')
    st.pyplot(fig)

def clusterizar_deforestacion(df):
    """Realiza un análisis de clúster sobre las superficies deforestadas.

    Args:
        df (pd.DataFrame): DataFrame con columnas 'lat', 'lon', 'superficie_deforestada'.
    """
    st.write("### Análisis de Clúster de Deforestación")
    df['cluster'] = np.digitize(df['superficie_deforestada'], bins=np.histogram_bin_edges(df['superficie_deforestada'], bins=3))
    fig, ax = plt.subplots()
    scatter = ax.scatter(df['lon'], df['lat'], c=df['cluster'], cmap='viridis')
    plt.colorbar(scatter)
    st.pyplot(fig)

def main():
    """Función principal para ejecutar la aplicación de análisis de deforestación."""
    st.title("Análisis de Deforestación")
    df = cargar_datos()
    if df is not None:
        mostrar_estadisticas(df)
        mostrar_mapa_deforestacion(df)
        clusterizar_deforestacion(df)

if __name__ == "__main__":
    main()

