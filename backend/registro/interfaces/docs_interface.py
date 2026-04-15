from abc import ABC, abstractmethod

from ..dtos import PDFResultDTO


class IDocsService(ABC):
    @abstractmethod
    def generar_pdf(self, datos_plantilla: dict) -> PDFResultDTO:
        """Copia la plantilla, reemplaza placeholders y exporta a PDF."""
        ...