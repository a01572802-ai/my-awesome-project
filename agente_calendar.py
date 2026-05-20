import json
from groq import Groq
from dotenv import load_dotenv
import os
from calendar_agent import conectar_calendar, crear_evento

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
service = conectar_calendar()

tools = [
    {
        "type": "function",
        "function": {
            "name": "crear_evento",
            "description": "Crea un evento en Google Calendar del usuario",
            "parameters": {
                "type": "object",
                "properties": {
                    "titulo": {"type": "string", "description": "Nombre del evento"},
                    "fecha": {
                        "type": "string",
                        "description": "Fecha en formato YYYY-MM-DD, ejemplo: 2026-05-23",
                    },
                    "hora_inicio": {
                        "type": "string",
                        "description": "Hora de inicio en formato HH:MM, ejemplo: 16:00",
                    },
                    "hora_fin": {
                        "type": "string",
                        "description": "Hora de fin en formato HH:MM, ejemplo: 17:00",
                    },
                },
                "required": ["titulo", "fecha", "hora_inicio", "hora_fin"],
            },
        },
    }
]


def agente(mensaje_usuario):
    # 1. Le mandamos el mensaje a Groq junto con las herramientas disponibles
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Eres un asistente que agrega eventos a Google Calendar. Hoy es 2026-05-19. Cuando el usuario mencione 'viernes' es 2026-05-22, 'mañana' es 2026-05-20, etc.",
            },
            {"role": "user", "content": mensaje_usuario},
        ],
        tools=tools,
    )

    # 2. Revisamos si la IA decidió llamar una función
    mensaje = response.choices[0].message

    if mensaje.tool_calls:
        # 3. La IA quiere llamar crear_evento — extraemos los parámetros
        tool_call = mensaje.tool_calls[0]
        parametros = json.loads(tool_call.function.arguments)

        print(f"IA detectó: {parametros}")

        # 4. Nosotros ejecutamos la función con esos parámetros
        link = crear_evento(
            service,
            parametros["titulo"],
            parametros["fecha"],
            parametros["hora_inicio"],
            parametros["hora_fin"],
        )

        print(f"Evento creado en tu Calendar: {link}")
    else:
        # La IA respondió con texto normal, no quiso llamar ninguna función
        print(f"IA: {mensaje.content}")


# Prueba
agente("ponme una junta el viernes a las 10 de la mañana, se llama revisión de proyecto, una hora")
