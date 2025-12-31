import streamlit as st
import streamlit as st
from gemini_assistant import ask_gemini

with st.expander("💎 Asistente Gemini (ayuda en código y desarrollo)"):
    user_question = st.text_input("Preguntale a Gemini sobre código, bugs, mejoras...", placeholder="Explica cómo agregar LoRA a diffusers")
    if st.button("Consultar Gemini"):
        with st.spinner("Gemini pensando..."):
            answer = ask_gemini(f"Eres un experto en Python, diffusers, Gradio y Streamlit. Responde en español: {user_question}")
            st.markdown(answer)

st.set_page_config(page_title="Multi-Tool AI Lab", layout="wide")

st.title("🚀 Multi-Tool AI Lab")
st.markdown("Generación de imágenes • Análisis de datos • Simulaciones físicas • Blender scripts")

tab1, tab2, tab3, tab4 = st.tabs(["Generador Imágenes", "Análisis Datos", "Simulaciones Física", "Blender Extensions"])

with tab1:
    st.header("Generador de Imágenes")
    # Aquí embed Gradio o código directo con diffusers
    st.write("Próximamente: Animagine XL / FLUX")

with tab2:
    st.header("Análisis de Datos")
    st.write("Subí CSV/Excel y analiza con Pandas")

with tab3:
    st.header("Simulaciones Físicas")
    st.write("PyBullet o Blender physics scripts")

with tab4:
    st.header("Blender Python Extensions")
    st.write("Ejecuta scripts bpy headless para simulaciones mecánicas, ray tracing batch, etc.")