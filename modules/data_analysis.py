import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def render():
    st.header("Análisis de Datos")
    st.markdown("Sube tus archivos CSV o Excel para realizar un análisis exploratorio rápido.")

    uploaded_file = st.file_uploader("Elige un archivo", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.subheader("Vista Previa de los Datos")
            st.dataframe(df.head())

            st.subheader("Estadísticas Descriptivas")
            st.write(df.describe())

            st.subheader("Información de Columnas")
            st.write(df.dtypes)

            st.subheader("Visualización")
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            if numeric_cols:
                col_x = st.selectbox("Selecciona eje X", numeric_cols)
                col_y = st.selectbox("Selecciona eje Y", numeric_cols)
                chart_type = st.radio("Tipo de gráfico", ["Dispersión (Scatter)", "Líneas", "Histograma"])

                fig, ax = plt.subplots()
                if chart_type == "Dispersión (Scatter)":
                    sns.scatterplot(data=df, x=col_x, y=col_y, ax=ax)
                elif chart_type == "Líneas":
                    sns.lineplot(data=df, x=col_x, y=col_y, ax=ax)
                else:
                    sns.histplot(df[col_x], kde=True, ax=ax)
                
                st.pyplot(fig)
                plt.close(fig)
            else:
                st.warning("No se encontraron columnas numéricas para graficar.")

        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")