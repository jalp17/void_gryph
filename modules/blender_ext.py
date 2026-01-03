import streamlit as st
from modules.assistant_client import ask_gemini

def render():
    st.header("Blender Python Extensions")
    st.markdown("""
    Genera y depura scripts de Python para Blender. 
    Debido a restricciones del entorno, estos scripts están diseñados para ser copiados y ejecutados en tu instancia local de Blender.
    """)

    script_type = st.selectbox("Tipo de Script", [
        "Crear Primitivas Aleatorias",
        "Animación de Rotación Básica",
        "Setup de Material Procedural",
        "Custom Script (Generado por Gemini)"
    ])

    if script_type == "Crear Primitivas Aleatorias":
        code = """import bpy
import random

def create_random_cubes(count=10):
    for i in range(count):
        x = random.uniform(-10, 10)
        y = random.uniform(-10, 10)
        z = random.uniform(0, 5)
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))

create_random_cubes(20)"""
    elif script_type == "Animación de Rotación Básica":
        code = """import bpy

obj = bpy.context.active_object
if obj:
    obj.animation_data_clear()
    obj.rotation_mode = 'XYZ'
    
    # Keyframe en frame 1
    obj.rotation_euler = (0, 0, 0)
    obj.keyframe_insert(data_path="rotation_euler", frame=1)
    
    # Keyframe en frame 100
    obj.rotation_euler = (0, 0, 6.28318) # 360 grados
    obj.keyframe_insert(data_path="rotation_euler", frame=100)"""
    elif script_type == "Setup de Material Procedural":
        code = """import bpy

def create_simple_material():
    mat = bpy.data.materials.new(name="AutoMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    
    # Limpiar nodos
    for node in nodes:
        nodes.remove(node)
        
    node_principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    node_principled.inputs['Base Color'].default_value = (0, 0.5, 0.8, 1)
    
    links = mat.node_tree.links
    links.new(node_principled.outputs[0], node_output.inputs[0])
    
    return mat

obj = bpy.context.active_object
if obj:
    obj.data.materials.append(create_simple_material())"""
    else:
        user_req = st.text_area("¿Qué quieres que haga el script de Blender?", "Crea un sistema de partículas simple que siga un path")
        if st.button("Generar con Gemini"):
            with st.spinner("Gemini redactando script..."):
                prompt = f"Escribe un script de Python para Blender (bpy) que haga lo siguiente: {user_req}. Solo el código, sin explicaciones largas."
                code = ask_gemini(prompt)
        else:
            code = "# Describe tu requerimiento arriba y presiona Generar"

    st.subheader("Código Generado")
    st.code(code, language="python")
    
    st.download_button("Descargar .py", code, file_name="blender_script.py")