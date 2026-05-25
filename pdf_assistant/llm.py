from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))


def responder(pregunta, contexto):
    respuesta = client_groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"Responde usando SOLO esta información:\n{contexto}\n\nSi no está en el documento, di que no lo sabes.",
            },
            {"role": "user", "content": pregunta},
        ],
    )
    return respuesta.choices[0].message.content
