from dataclasses import dataclass

@dataclass
class PollenDTO:
    tipo_polen: str
    estado: str
    datos_detalle: str