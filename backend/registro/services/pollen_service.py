import requests
from datetime import datetime

from ..dtos import CoordenadasDTO, PollenDTO
from ..interfaces import IPollenService
from ..constants import ALERGENO_MAP

def _nivel_riesgo(valor: float) -> str:
    if valor < 10:    return 'Bajo'
    if valor < 50:    return 'Moderado'
    if valor < 200:   return 'Alto'
    return 'Muy alto'


class PollenService(IPollenService):
    BASE_URL = 'https://air-quality-api.open-meteo.com/v1/air-quality'

    def obtener_datos_polen(
        self,
        coordenadas: CoordenadasDTO,
        alergias: list[str],
    ) -> PollenDTO:
        variables = [
            ALERGENO_MAP[alergia['nombre']] for alergia in alergias
            if alergia['nombre'] in ALERGENO_MAP and ALERGENO_MAP[alergia['nombre']] is not None
        ]

        if not variables:
            return PollenDTO(
                tipo_polen='Sin datos',
                estado='Sin datos',
                datos_detalle='No hay alérgenos medibles por Open-Meteo para tus alergias registradas.',
            )

        response = requests.get(
            self.BASE_URL,
            params={
                'latitude': coordenadas.latitud,
                'longitude': coordenadas.longitud,
                'hourly': ','.join(variables),
                'timezone': 'Europe/Madrid',
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        hora_actual = datetime.now().hour
        valores = {}
        for var in variables:
            serie = data['hourly'].get(var, [])
            valores[var] = serie[hora_actual] if hora_actual < len(serie) else 0.0

        principal_var = max(valores, key=valores.get)
        principal_valor = valores[principal_var]
        principal_nombre = next(k for k, v in ALERGENO_MAP.items() if v == principal_var)

        estado = _nivel_riesgo(principal_valor)

        detalle_lineas = [
            f'- {next(k for k, v in ALERGENO_MAP.items() if v == var)}: {round(valor, 1)} gr/m³ ({_nivel_riesgo(valor)})'
            for var, valor in valores.items()
        ]

        return PollenDTO(
            tipo_polen=principal_nombre,
            estado=estado,
            datos_detalle='\n'.join(detalle_lineas),
        )