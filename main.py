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

def interpolate_data(df, method):
    """Rellena los valores faltantes en el DataFrame usando el método de interpolación seleccionado."""
    return df.interpolate(method=method, limit_direction='both')

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
        st.write(data.head())

        # Opción para seleccionar el método de interpolación
        method = st.selectbox("Selecciona el método de interpolación", ['linear', 'polynomial', 'spline', 'barycentric', 'pchip'])

        # Interpolar los datos
        interpolated_data = interpolate_data(data, method)

        # Mostrar el DataFrame con los valores interpolados
        st.write("Datos después de la interpolación:")
        st.write(interpolated_data)

        # Descargar el archivo interpolado
        csv = interpolated_data.to_csv(index=False)
        st.download_button(
            label="Descargar archivo interpolado",
            data=csv,
            file_name="datos_interpolados.csv",
            mime="text/csv"
        )
    else:
        st.warning("Por favor, carga un archivo o ingresa una URL válida.")

if __name__ == "__main__":
    main()
