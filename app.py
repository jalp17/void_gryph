import streamlit as st
from modules.assistant_client import ask_gemini
from modules import image_gen, data_analysis, physics_sim, blender_ext

st.set_page_config(page_title="Multi-Tool AI Lab", layout="wide")

with st.expander("💎 Asistente Gemini (ayuda en código y desarrollo)"):
    user_question = st.text_input("Preguntale a Gemini sobre código, bugs, mejoras...", placeholder="Explica cómo agregar LoRA a diffusers")
    if st.button("Consultar Gemini"):
        with st.spinner("Gemini pensando..."):
            answer = ask_gemini(f"Eres un experto en Python, diffusers, Gradio y Streamlit. Responde en español: {user_question}")
            st.markdown(answer)

st.title("🚀 Multi-Tool AI Lab")
st.markdown("Generación de imágenes • Análisis de datos • Simulaciones físicas • Blender scripts")

tab1, tab2, tab3, tab4 = st.tabs(["Generador Imágenes", "Análisis Datos", "Simulaciones Física", "Blender Extensions"])

with tab1:
    image_gen.render()

with tab2:
    data_analysis.render()

with tab3:
    physics_sim.render()

with tab4:
    blender_ext.render()
