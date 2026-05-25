from pypdf import PdfReader


def leer_pdf(archivo):
    reader = PdfReader(archivo)
    texto_completo = ""
    for pagina in reader.pages:
        texto_completo += pagina.extract_text()
    return texto_completo


def dividir_chunks(texto, chunk_size=500):
    chunks = []
    for i in range(0, len(texto), chunk_size):
        chunk = texto[i : i + chunk_size]
        if chunk.strip():
            chunks.append(chunk)
    return chunks
