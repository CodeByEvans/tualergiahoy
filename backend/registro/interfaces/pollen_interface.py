from abc import ABC, abstractmethod

from ..dtos import CoordenadasDTO, PollenDTO


class IPollenService(ABC):
    @abstractmethod
    def obtener_datos_polen(
        self,
        coordenadas: CoordenadasDTO,
        alergias: list[str],
    ) -> PollenDTO:
        """Obtiene los niveles de polen actuales para las alergias indicadas."""
        ...