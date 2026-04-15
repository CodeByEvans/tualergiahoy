from abc import ABC, abstractmethod

from ..dtos import PollenDTO, PDFResultDTO


class IEmailService(ABC):
    @abstractmethod
    def enviar_bienvenida(
        self,
        destinatario: str,
        nombre: str,
        datos_polen: PollenDTO,
        pdf: PDFResultDTO,
    ) -> None:
        """Envía el email de bienvenida con el PDF adjunto."""
        ...