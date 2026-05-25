from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

# 1. Leer el PDF
reader = PdfReader("ae10.pdf")
texto_completo = ""
for pagina in reader.pages:
    texto_completo += pagina.extract_text()

print(f"PDF leído: {len(texto_completo)} caracteres")

# 2. Dividir en chunks
def dividir_texto(texto, chunk_size=500):
    chunks = []
    for i in range(0, len(texto), chunk_size):
        chunk = texto[i:i + chunk_size]
        if chunk.strip():
            chunks.append(chunk)
    return chunks

chunks = dividir_texto(texto_completo)
print(f"Chunks creados: {len(chunks)}")

# 3. Guardar en ChromaDB
model = SentenceTransformer('all-MiniLM-L6-v2')
client_db = chromadb.Client()
collection = client_db.get_or_create_collection(name="pdf_actividad")

for i, chunk in enumerate(chunks):
    embedding = model.encode(chunk).tolist()
    collection.add(
        ids=[str(i)],
        embeddings=[embedding],
        documents=[chunk]
    )

print(f"Guardados {collection.count()} chunks en ChromaDB ✓")

# 4. Hacer preguntas
client_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

def preguntar_pdf(pregunta):
    # Buscar chunks relevantes
    embedding_pregunta = model.encode(pregunta).tolist()
    resultados = collection.query(
        query_embeddings=[embedding_pregunta],
        n_results=3
    )
    
    contexto = "\n".join(resultados['documents'][0])
    
    respuesta = client_groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"""Eres un asistente que responde preguntas sobre un documento.
Usa SOLO esta información para responder:
{contexto}

Si la respuesta no está en el documento, di que no lo sabes."""
            },
            {
                "role": "user",
                "content": pregunta
            }
        ]
    )
    return respuesta.choices[0].message.content

# Prueba
print(preguntar_pdf("¿De qué trata el proyecto?"))