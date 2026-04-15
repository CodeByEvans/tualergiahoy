from dataclasses import dataclass

@dataclass
class PDFResultDTO:
    contenido: bytes
    nombre_archivo: str
