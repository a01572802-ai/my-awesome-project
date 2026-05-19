from def_grok import preguntar

with open("system_prompt.txt", "r") as file:
    system_prompt = file.read()

historial = [{"role": "system", "content": system_prompt}]

while True:
    mensaje = input("Tú: ")

    if mensaje == "salir":
        break

    historial.append({"role": "user", "content": mensaje})
    respuesta = preguntar(historial)
    historial.append({"role": "assistant", "content": respuesta})

    print(f"IA: {respuesta}\n")
