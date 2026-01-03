import streamlit as st
import pybullet as p
import time
import pandas as pd
import matplotlib.pyplot as plt

def run_simple_sim(gravity, initial_height):
    # Conexión en modo DIRECT (headless)
    physicsClient = p.connect(p.DIRECT)
    p.setGravity(0, 0, gravity)
    
    # Crear un plano
    planeId = p.createCollisionShape(p.GEOM_PLANE)
    p.createMultiBody(0, planeId)
    
    # Crear una esfera
    sphereShape = p.createCollisionShape(p.GEOM_SPHERE, radius=0.1)
    sphereId = p.createMultiBody(1, sphereShape, basePosition=[0, 0, initial_height])
    
    data = []
    # Simular por 240 pasos (aprox 1 segundo a 240Hz por defecto)
    for i in range(240):
        p.stepSimulation()
        pos, ori = p.getBasePositionAndOrientation(sphereId)
        data.append({"step": i, "z_position": pos[2]})
        if pos[2] <= 0.1: # Golpeó el suelo
            break
            
    p.disconnect()
    return pd.DataFrame(data)

def render():
    st.header("Simulaciones Físicas")
    st.markdown("Configura y ejecuta simulaciones físicas simples usando **PyBullet** (Headless).")

    col1, col2 = st.columns(2)
    with col1:
        gravity = st.slider("Gravedad (m/s²)", -20.0, 0.0, -9.81)
    with col2:
        height = st.slider("Altura inicial (m)", 1.0, 50.0, 10.0)

    if st.button("Ejecutar Simulación de Caída"):
        with st.spinner("Simulando..."):
            df = run_simple_sim(gravity, height)
            
            st.success("Simulación completada.")
            
            st.subheader("Trayectoria de Caída (Z)")
            fig, ax = plt.subplots()
            ax.plot(df['step'], df['z_position'], label='Posición Z')
            ax.set_xlabel('Pasos de simulación')
            ax.set_ylabel('Altura (m)')
            ax.legend()
            st.pyplot(fig)
            plt.close(fig)
            
            st.subheader("Datos de la simulación")
            st.dataframe(df.tail())