from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def conectar_calendar():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)


def crear_evento(service, titulo, fecha, hora_inicio, hora_fin):
    evento = {
        "summary": titulo,
        "start": {
            "dateTime": f"{fecha}T{hora_inicio}:00",
            "timeZone": "America/Monterrey",
        },
        "end": {"dateTime": f"{fecha}T{hora_fin}:00", "timeZone": "America/Monterrey"},
    }
    resultado = service.events().insert(calendarId="primary", body=evento).execute()
    return resultado.get("htmlLink")
