import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Modelo rápido y potente para código
model = genai.GenerativeModel('gemini-1.5-flash')  # o 'gemini-1.5-pro' si querés más potencia

def ask_gemini(prompt: str):
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print("🤖 Gemini:", ask_gemini(query))
    else:
        print("Uso: python gemini_assistant.py 'tu pregunta sobre código'")