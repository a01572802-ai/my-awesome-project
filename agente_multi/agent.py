from tools.weather import get_weather_tempt_city
from tools.time_tool import get_time
from tools.search import search_web
from groq import Groq
from dotenv import load_dotenv
import os
import json
import sys

sys.path.append(os.path.dirname(__file__))

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


MODELOS = [
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "llama-3.3-70b-versatile",
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather_tempt_city",
            "description": "Obtiene el clima de una ciudad",
            "parameters": {
                "type": "object",
                "properties": {
                    "city_name": {
                        "type": "string",
                        "description": "Nombre de la ciudad",
                    }
                },
                "required": ["city_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Obtiene la hora actual de una zona horaria",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone_str": {
                        "type": "string",
                        "description": "Zona horaria en formato continent/city, ejemplo: America/Monterrey",
                    }
                },
                "required": ["timezone_str"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Busca información sobre cualquier tema",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Lo que se quiere buscar",
                    }
                },
                "required": ["query"],
            },
        },
    },
]


def agente(mensaje):
    for modelo in MODELOS:
        try:
            response = client.chat.completions.create(
                model=modelo,
                messages=mensaje,
                tools=tools,
                disable_tool_validation=True,
            )
            respuesta_ia = response.choices[0].message

            if respuesta_ia.tool_calls:
                tool_call = respuesta_ia.tool_calls[0]
                nombre_herramienta = tool_call.function.name
                parametros = json.loads(tool_call.function.arguments)

                if nombre_herramienta == "get_weather_tempt_city":
                    resultado = get_weather_tempt_city(parametros["city_name"])
                elif nombre_herramienta == "get_time":
                    resultado = get_time(parametros["timezone_str"])
                elif nombre_herramienta == "search_web":
                    resultado = search_web(parametros["query"])

                mensaje.append({"role": "assistant", "content": str(resultado)})
                print(f"Resultado: {resultado}")
            else:
                print(f"IA: {respuesta_ia.content}")
                mensaje.append({"role": "assistant", "content": respuesta_ia.content})
            return

        except Exception as e:
            print(f"Modelo {modelo} falló, intentando siguiente...")
            continue

    print("Todos los modelos fallaron. Intenta de nuevo.")
