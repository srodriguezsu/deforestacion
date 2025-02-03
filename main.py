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

def analizar_deforestacion(df):
    """Realiza un análisis básico de deforestación a partir de un DataFrame con las columnas 'año', 'superficie_total', 'superficie_deforestada'."""
    
    # Asegúrate de que los datos estén en el tipo adecuado (números)
    df['superficie_total'] = df['superficie_total'].astype(float)
    df['superficie_deforestada'] = df['superficie_deforestada'].astype(float)
    
    # Calcula la superficie deforestada anual (si los datos no están en términos anuales)
    df['superficie_deforestada_anual'] = df['superficie_deforestada'].diff().fillna(0)
    
    # Calcula la tasa de deforestación anual
    df['tasa_deforestacion'] = df['superficie_deforestada_anual'] / df['superficie_total']
    
    # Calcula el porcentaje de deforestación con respecto a la superficie total
    df['porcentaje_deforestado'] = (df['superficie_deforestada'] / df['superficie_total']) * 100
    
    # Resultados generales
    superficie_total_inicial = df['superficie_total'].iloc[0]
    superficie_total_final = df['superficie_total'].iloc[-1]
    superficie_deforestada_total = df['superficie_deforestada'].iloc[-1]
    
    tasa_deforestacion_total = df['tasa_deforestacion'].sum()
    
    # Mostrar los resultados de análisis
    st.write(f"Superficie total inicial: {superficie_total_inicial} ha")
    st.write(f"Superficie total final: {superficie_total_final} ha")
    st.write(f"Superficie deforestada total: {superficie_deforestada_total} ha")
    st.write(f"Tasa total de deforestación: {tasa_deforestacion_total:.4f}")
    
    # Mostrar la tabla con los resultados
    st.write(df)
    
    # Gráficos para visualizar las tendencias
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    # Gráfico de la superficie deforestada anual
    ax[0].plot(df['año'], df['superficie_deforestada_anual'], marker='o', color='tab:red')
    ax[0].set_title('Superficie deforestada anual')
    ax[0].set_xlabel('Año')
    ax[0].set_ylabel('Área deforestada (ha)')
    
    # Gráfico de porcentaje de deforestación
    ax[1].plot(df['año'], df['porcentaje_deforestado'], marker='o', color='tab:blue')
    ax[1].set_title('Porcentaje de deforestación')
    ax[1].set_xlabel('Año')
    ax[1].set_ylabel('Porcentaje (%)')

    st.pyplot(fig)
        

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
        data = data.interpolate(method='linear')
        
        st.write(data)
        analizar_deforestacion(data)
        
    else:
        st.warning("Por favor, carga un archivo o ingresa una URL válida.")


if __name__ == "__main__":
    main()
