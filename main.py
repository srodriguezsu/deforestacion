import streamlit as st
import pandas as pd
import numpy as np

def load_data(file=None, url=None):
    """Carga los datos desde un archivo o una URL."""
    if file is not None:
        return pd.read_csv(file)
    elif url is not None:
        return pd.read_csv(url)
    else:
        return None

def infer_and_convert_data(df):
    """Infiera el tipo de dato y convierte las columnas numéricas a tipo float para la interpolación."""
    # Seleccionar solo las columnas numéricas
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    # Convertir todas las columnas numéricas a float
    df[numeric_cols] = df[numeric_cols].astype(float)
    return df


def main():
    st.title('Aplicación de Interpolación de Datos')

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
        data = infer_and_convert_data(data)
        interpolado = data.interpolate(method='linear')
        
        st.write(interpolado)
        
    else:
        st.warning("Por favor, carga un archivo o ingresa una URL válida.")


if __name__ == "__main__":
    main()
