FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependencias sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    git wget libgl1 libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Crea usuario
RUN useradd -m -u 1000 user
USER user
WORKDIR /app

# Instala torch CPU desde index oficial
RUN pip install --user --no-cache-dir --index-url https://download.pytorch.org/whl/cpu \
    torch torchvision torchaudio

# Instala el resto (diffusers ahora encuentra torch compatible)
COPY --chown=user:user requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

COPY --chown=user:user . .

ENV PATH="/home/user/.local/bin:${PATH}"

# Instala Gemini SDK (oficial de Google)
RUN pip install --user --no-cache-dir google-genai

# Alias opcional
RUN echo 'alias gemini="python -m google.genai"' >> /home/user/.bashrc

EXPOSE 7860

CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]