import os
import pickle

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from django.conf import settings

from ..interfaces import IGoogleAuthService

SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive',
]


class GoogleAuthService(IGoogleAuthService):
    """
    Responsabilidad: gestionar las credenciales OAuth2 de Google.
    Obtiene, refresca y persiste el token del usuario.
    """

    TOKEN_PATH = 'token.pickle'

    def obtener_credenciales(self) -> Credentials:
        creds = self._cargar_token()

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                creds = self._autorizar()
            self._guardar_token(creds)

        return creds

    def _cargar_token(self) -> Credentials | None:
        if os.path.exists(self.TOKEN_PATH):
            with open(self.TOKEN_PATH, 'rb') as f:
                return pickle.load(f)
        return None

    def _guardar_token(self, creds: Credentials) -> None:
        with open(self.TOKEN_PATH, 'wb') as f:
            pickle.dump(creds, f)

    def _autorizar(self) -> Credentials:
        flow = InstalledAppFlow.from_client_secrets_file(
            settings.GOOGLE_OAUTH_CREDENTIALS_PATH,
            SCOPES,
        )
        return flow.run_local_server(port=0)