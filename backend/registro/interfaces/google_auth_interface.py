from google.oauth2.credentials import Credentials
from abc import ABC, abstractmethod

class IGoogleAuthService(ABC):
    @abstractmethod
    def obtener_credenciales(self) -> Credentials:
        pass
    
    @abstractmethod
    def _cargar_token(self) -> Credentials | None:
        pass
    
    @abstractmethod
    def _guardar_token(self, creds: Credentials) -> None:
        pass
    
    @abstractmethod
    def _autorizar(self) -> Credentials:
        pass