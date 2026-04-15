from abc import ABC, abstractmethod

from ..dtos import CoordenadasDTO


class IGeocodingService(ABC):
    @abstractmethod
    def obtener_coordenadas(self, ciudad: str) -> CoordenadasDTO:
        """Convierte un nombre de ciudad en coordenadas geográficas."""
        ...