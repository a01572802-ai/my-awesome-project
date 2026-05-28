from datetime import datetime
import pytz


def get_time(timezone_str):
    try:
        zona = pytz.timezone(timezone_str)
        hora_actual = datetime.now(zona)
        return {
            "timezone": timezone_str,
            "hora": hora_actual.strftime("%H:%M"),
            "fecha": hora_actual.strftime("%Y-%m-%d"),
        }
    except pytz.exceptions.UnknownTimeZoneError:
        return {"error": f"Zona horaria no encontrada: {timezone_str}"}
