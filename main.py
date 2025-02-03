import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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
        
    else:
        st.warning("Por favor, carga un archivo o ingresa una URL válida.")


if __name__ == "__main__":
    main()
