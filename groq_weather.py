from def_weather import get_weather_tempt_city
from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
historial = []

tools = [
    {
        "type": "function",
        "function": {
            "name": "clima",
            "description": "Proporciona el clima con esta estructura",
            "parameters": {
                "type": "object",
                "properties": {
                    "city_name": {
                        "type": "string",
                        "description": "Nombre de la ciudad a la que se le quiere sacar el clima",
                    },
                },
                "required": ["city_name"],
            },
        },
    }
]


def agente(mensaje_usuario):
    historial.append({"role": "user", "content": mensaje_usuario})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Eres un asistente personal. SOLO usa la herramienta 'clima' cuando el usuario explícitamente pregunte por el clima o la temperatura de una ciudad. Para cualquier otra pregunta responde normalmente.",
            },
        ]
        + historial,
        tools=tools,
    )
    respuesta_ia = response.choices[0].message
    if respuesta_ia.tool_calls:
        tool_call = respuesta_ia.tool_calls[0]
        parametros = json.loads(tool_call.function.arguments)

        data = get_weather_tempt_city(parametros["city_name"])
        print(f"El clima de {parametros['city_name']} es: {data}")
    else:
        print(f"IA: {respuesta_ia.content}")
    historial.append({"role": "assistant", "content": respuesta_ia.content})


while True:
    texto_usuario = input("Tú: ")
    if texto_usuario == "salir":
        break
    agente(texto_usuario)
