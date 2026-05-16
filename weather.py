import requests
from dotenv import load_dotenv
import os


load_dotenv(".env")
api_key = os.getenv("API_KEY")
lat = 25.755746
lon = -100.411714

url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    print(f"Ciudad: Monterrey, {data['sys']['country']}")
    print(f"Temperatura: {data['main']['temp']:.1f}")
    print(f"Clima: {data['weather'][0]['main']}")
except requests.exceptions.HTTPError as e:
    print(f"Error de API: {e}")
except requests.exceptions.ConnectionError:
    print("Sin conexión a internet")
