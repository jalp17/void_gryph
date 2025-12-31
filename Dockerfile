# Usa imagen base oficial Python slim (ligera)
FROM python:3.11-slim

# Variables de entorno para mejor performance
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependencias del sistema (para torch CUDA, Blender bpy, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    wget \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Crea usuario no-root (seguridad recomendada por HF)
RUN useradd -m -u 1000 user
USER user
WORKDIR /app

# Copia requirements y instala en .local
COPY --chown=user:user requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copia el resto de la app
COPY --chown=user:user . .

# Hace .local/bin accesible
ENV PATH="/home/user/.local/bin:${PATH}"

# Puerto estándar para web apps en HF Spaces
EXPOSE 7860

# Comando de inicio (usa Streamlit por default, cambia si querés Gradio)
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]