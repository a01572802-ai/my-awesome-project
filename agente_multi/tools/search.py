def search_web(query):
    return {
        "query": query,
        "resultados": [
            {
                "titulo": f"Todo sobre {query} - Wikipedia",
                "descripcion": f"{query} es un tema ampliamente documentado con múltiples aplicaciones en la industria tecnológica.",
                "url": "wikipedia.org"
            },
            {
                "titulo": f"Guía completa de {query} 2026",
                "descripcion": f"Aprende todo lo que necesitas saber sobre {query} con ejemplos prácticos y casos de uso reales.",
                "url": "medium.com"
            },
            {
                "titulo": f"¿Qué es {query}? Explicado simple",
                "descripcion": f"Una explicación clara y sencilla de {query} para principiantes y expertos.",
                "url": "dev.to"
            }
        ]
    }