import sys
import os
sys.path.append(os.path.dirname(__file__))

from agent import agente

mensaje = []

while True:
    texto = input("Tú: ")
    if texto == "salir":
        break
    mensaje.append({"role": "user", "content": texto})
    agente(mensaje)