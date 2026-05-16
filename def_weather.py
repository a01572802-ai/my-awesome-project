import requests
from dotenv import load_dotenv
import os

load_dotenv(".env")


def get_weather_tempt_city(city_name):
    city = city_name
    api_key = os.getenv("API_KEY")
    url_city = (
        f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    )

    try:
        city_data = requests.get(url_city)
        city_data.raise_for_status
        city_data_json = city_data.json()
        if not city_data_json:
            print(f"No se encontró la ciudad: {city_name}")
            return
        lat = city_data_json[0]["lat"]
        lon = city_data_json[0]["lon"]
    except requests.exceptions.RequestException as e:
        print(f"Error al buscar la ciudad: {e}")
        return

    url_data = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"

    try:
        response = requests.get(url_data)
        response.raise_for_status()
        data = response.json()
        return {
            "ciudad": city_name.capitalize(),
            "pais": data["sys"]["country"],
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "descripcion": data["weather"][0]["description"],
        }
    except requests.exceptions.HTTPError as e:
        print(f"Error de API: {e}")
    except requests.exceptions.ConnectionError:
        print("Sin conexión a internet")
