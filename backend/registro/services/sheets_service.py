import gspread
from google.oauth2.service_account import Credentials
from django.conf import settings
from ..dtos.sheets_dto import SheetsRegistroDTO

from ..interfaces import ISheetsService

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class SheetsService(ISheetsService):
    def __init__(self):
        creds = Credentials.from_service_account_file(
            settings.GOOGLE_CREDENTIALS_PATH,
            scopes=SCOPES,
        )
        self._client = gspread.authorize(creds)
        self._sheet = self._client.open_by_key(settings.GOOGLE_SHEETS_ID).sheet1

def insertar_registro(self, datos: SheetsRegistroDTO) -> None:
    fila = [
        str(datos.id),
        datos.nombre,
        datos.apellidos,
        datos.fecha_nacimiento,
        datos.ciudad,
        datos.email,
        datos.telefono,
        datos.alergias,
        datos.medicacion,
        'Sí' if datos.acepta_notificaciones else 'No',
        datos.nivel_riesgo,
        datos.como_nos_conocio,
        datos.fecha_registro,
    ]

    self._sheet.append_row(fila, value_input_option='USER_ENTERED')