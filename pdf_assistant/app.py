import streamlit as st
from pdf_processor import leer_pdf, dividir_chunks
from vector_store import guardar_chunks, buscar_chunks, get_collection
from llm import responder
st.title("📄 Asistente de PDFs")
st.write("Sube un PDF y hazle preguntas")

pdf = st.file_uploader("Sube tu PDF", type="pdf")

if pdf:
    texto = leer_pdf(pdf)
    chunks = dividir_chunks(texto)
    collection = get_collection()
    guardar_chunks(chunks, collection)
    st.success(f"PDF procesado — {len(chunks)} secciones listas ✓")

    pregunta = st.text_input("¿Qué quieres saber del PDF?")

    if st.button("Preguntar"):
        if pregunta:
            with st.spinner("Buscando respuesta..."):
                contexto = buscar_chunks(pregunta, collection)
                respuesta = responder(pregunta, contexto)
                st.write(respuesta)
        else:
            st.warning("Escribe una pregunta primero")



