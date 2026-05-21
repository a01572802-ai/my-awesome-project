from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analizar_nombre(nombre):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """Eres una IA que analiza personas basándote en toda la información que te dan.
                Responde SOLO con JSON, sin texto extra, con una explicacion medio muy corta explicaciones, sin bloques de código.
                Usa exactamente esta estructura:
                {"nombre": "...", "edad_estimada": 0, "origen_probable": "...", "explicacion_del_analisis": "..."}"""
            },
            {
                "role": "user",
                "content": nombre
            }
        ]
    )
    return response.choices[0].message.content

resultado = analizar_nombre("Axel, edad estoy en prepa tec voy a pasar a quinto semestre, soy de mexico")
datos = json.loads(resultado)
print(datos["nombre"])
print(datos["edad_estimada"])
print(datos["origen_probable"])
print(datos["explicacion_del_analisis"])
