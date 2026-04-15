from abc import ABC, abstractmethod


class ISheetsService(ABC):
    @abstractmethod
    def insertar_registro(self, datos: dict) -> None:
        """Inserta una fila en Google Sheets con los datos del registro."""
        ...
