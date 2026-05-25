import streamlit as st
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
from groq import Groq
from dotenv import load_dotenv
import os
import io

load_dotenv()

st.title("📄 Asistente de PDFs")
st.write("Sube un PDF y hazle preguntas")

# Cargar modelos una sola vez
@st.cache_resource
def cargar_modelos():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    client_db = chromadb.Client()
    client_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return model, client_db, client_groq

model, client_db, client_groq = cargar_modelos()

pdf = st.file_uploader("Sube tu PDF", type="pdf")

if pdf:
    # Leer PDF
    reader = PdfReader(io.BytesIO(pdf.read()))
    texto = ""
    for pagina in reader.pages:
        texto += pagina.extract_text()

    # Dividir en chunks y guardar
    chunks = [texto[i:i+500] for i in range(0, len(texto), 500) if texto[i:i+500].strip()]
    
    collection = client_db.get_or_create_collection(name="pdf_app")
    collection.delete(where={"source": "pdf"})
    
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()
        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{"source": "pdf"}]
        )

    st.success(f"PDF procesado — {len(chunks)} secciones listas ✓")

    # Pregunta
    pregunta = st.text_input("¿Qué quieres saber del PDF?")

    if st.button("Preguntar"):
        if pregunta:
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
                        "content": f"Responde usando SOLO esta información:\n{contexto}\n\nSi no está en el documento, di que no lo sabes."
                    },
                    {"role": "user", "content": pregunta}
                ]
            )
            st.write(respuesta.choices[0].message.content)