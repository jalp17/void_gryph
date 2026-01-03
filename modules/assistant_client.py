import sys
import os

# Forzar la prioridad del entorno virtual si existe (útil en Codespaces)
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
venv_site_packages = os.path.join(base_path, ".venv", "lib", "python3.12", "site-packages")

if os.path.exists(venv_site_packages) and venv_site_packages not in sys.path:
    sys.path.insert(0, venv_site_packages)

try:
    from google import genai
except ImportError:
    # Fallback para entornos donde el namespace es problemático
    try:
        import google_genai as genai
    except ImportError:
        pass

# Inicializar el cliente con la nueva sintaxis oficial
def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key or api_key.strip() == "":
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception:
        return None

def ask_gemini(prompt: str):
    client = get_client()
    if not client:
        return "⚠️ **Error**: No se configuró la variable `GEMINI_API_KEY`. Por favor, configúrala en los Secrets o terminal."
    
    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        # Intento de fallback automático a otro modelo común
        try:
            response = client.models.generate_content(
                model='gemini-1.5-pro',
                contents=prompt
            )
            return response.text
        except:
            return f"❌ **Error en la API de Gemini**: {e}"
