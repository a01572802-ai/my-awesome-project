from def_weather import get_weather_tempt_city

resultado = get_weather_tempt_city(input("City name: "))
if resultado:
    print(f"Ciudad: {resultado['ciudad']}, {resultado['pais']}")
    print(f"Temperatura: {resultado['temp']:.1f}°C")
    print(f"Clima: {resultado['descripcion']}")


