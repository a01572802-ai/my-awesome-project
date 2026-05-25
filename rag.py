import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

# Crear base de datos vectorial en memoria
client = chromadb.Client()
collection = client.get_or_create_collection(name="apuntes")

# Tus apuntes de ejemplo
apuntes = [
    "Python es un lenguaje de programación de alto nivel",
    "Un loop for sirve para repetir código varias veces",
    "Las funciones se definen con la palabra def",
    "Un diccionario guarda datos en pares clave-valor",
    "Los embeddings convierten texto en números",
]

# Guardar cada apunte en ChromaDB
for i, apunte in enumerate(apuntes):
    embedding = model.encode(apunte).tolist()
    collection.add(ids=[str(i)], embeddings=[embedding], documents=[apunte])

print(f"Guardados {collection.count()} apuntes en ChromaDB ✓")

# Pregunta del usuario
pregunta = "¿cómo repito código?"

# Convertir la pregunta en embedding y buscar
embedding_pregunta = model.encode(pregunta).tolist()
resultados = collection.query(query_embeddings=[embedding_pregunta], n_results=2)

print(f"Pregunta: {pregunta}")
print(f"Apuntes más relevantes:")
for doc in resultados["documents"][0]:
    print(f"  - {doc}")


load_dotenv()
client_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

contexto = "\n".join(resultados["documents"][0])

respuesta = client_groq.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": f"""Responde la pregunta del usuario usando SOLO esta información:
{contexto}

Si la respuesta no está en la información, di que no lo sabes.""",
        },
        {"role": "user", "content": pregunta},
    ],
)

print(f"\nRespuesta de la IA:")
print(respuesta.choices[0].message.content)
