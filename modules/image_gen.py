import streamlit as st
import os

@st.cache_resource
def load_pipeline():
    import torch
    from diffusers import StableDiffusionPipeline
    # Usamos float32 para CPU
    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32, use_safetensors=True)
    # Optimizaciones para CPU
    pipe.enable_attention_slicing()
    return pipe

def render():
    st.header("Generador de Imágenes")
    st.markdown("Generación de imágenes usando Stable Diffusion v1.5 optimizado para CPU.")

    prompt = st.text_input("Prompt positivo", "A futuristic city with flying cars, cyberpunk style, high detail")
    negative_prompt = st.text_input("Prompt negativo", "low quality, blurry, bad anatomy")
    
    col1, col2 = st.columns(2)
    with col1:
        num_steps = st.slider("Pasos de inferencia", 1, 50, 20)
    with col2:
        guidance_scale = st.slider("Escala de guía (CFG)", 1.0, 20.0, 7.5)

    if st.button("Generar Imagen"):
        with st.spinner("Cargando modelo y generando... (esto puede tardar varios minutos en CPU)"):
            try:
                pipe = load_pipeline()
                # En CPU no usamos autocast o movemos a cuda
                image = pipe(
                    prompt, 
                    negative_prompt=negative_prompt, 
                    num_inference_steps=num_steps,
                    guidance_scale=guidance_scale
                ).images[0]
                
                st.image(image, caption=f"Resultado: {prompt}", use_column_width=True)
                
                # Opción de descarga
                import io
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                byte_im = buf.getvalue()
                st.download_button(
                    label="Descargar Imagen",
                    data=byte_im,
                    file_name="generated_image.png",
                    mime="image/png"
                )
            except Exception as e:
                st.error(f"Error al generar la imagen: {e}")
                st.info("Asegurate de tener suficiente RAM (mínimo 8GB-12GB libres para SD v1.5 en CPU).")