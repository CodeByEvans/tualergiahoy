from abc import ABC, abstractmethod

from ..dtos import PollenDTO


class IAIService(ABC):
    @abstractmethod
    def generar_prevision(
        self,
        nombre: str,
        ciudad: str,
        alergias: list[dict],
        datos_polen: PollenDTO,
    ) -> str:
        """Genera un pronóstico personalizado usando IA."""
        ...