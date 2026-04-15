from dataclasses import dataclass

@dataclass
class CoordenadasDTO:
    latitud: float
    longitud: float
    ciudad: str