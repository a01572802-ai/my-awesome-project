from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer("all-MiniLM-L6-v2")

texto = "Python es un lenguaje de programación"
embedding = model.encode(texto)

print(f"Texto: {texto}")
print(f"Cuántos números tiene: {embedding.shape}")
print(f"Primeros 5 números: {embedding[:5]}")


textos = [
    "Python es un lenguaje de programación",
    "Me gustan los tacos de canasta",
    "JavaScript también es un lenguaje de programación",
]

embeddings = model.encode(textos)

# Comparar el primer texto con los demás
similitud_1 = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
similitud_2 = cosine_similarity([embeddings[0]], [embeddings[2]])[0][0]

print(f"'{textos[0]}' vs '{textos[1]}'")
print(f"Similitud: {similitud_1:.2f}\n")

print(f"'{textos[0]}' vs '{textos[2]}'")
print(f"Similitud: {similitud_2:.2f}")
