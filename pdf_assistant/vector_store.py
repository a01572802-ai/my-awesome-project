from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")
client_db = chromadb.Client()


def guardar_chunks(chunks, collection):
    collection.delete(where={"source": "pdf"})
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()
        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{"source": "pdf"}],
        )


def buscar_chunks(pregunta, collection, n_results=3):
    embedding_pregunta = model.encode(pregunta).tolist()
    resultados = collection.query(
        query_embeddings=[embedding_pregunta], n_results=n_results
    )
    return "\n".join(resultados["documents"][0])


def get_collection():
    return client_db.get_or_create_collection(name="pdf_app")
