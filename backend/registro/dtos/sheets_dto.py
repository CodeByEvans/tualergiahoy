from dataclasses import dataclass

@dataclass
class SheetsRegistroDTO:
    id: int
    nombre: str
    apellidos: str
    fecha_nacimiento: str
    ciudad: str
    email: str
    telefono: str
    alergias: str
    medicacion: str
    acepta_notificaciones: bool
    nivel_riesgo: str
    como_nos_conocio: str
    fecha_registro: str