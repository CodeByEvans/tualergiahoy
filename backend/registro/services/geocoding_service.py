import requests
from django.conf import settings

from ..dtos import CoordenadasDTO
from ..interfaces import IGeocodingService



class GeocodingService(IGeocodingService):
    BASE_URL = 'https://geocoding-api.open-meteo.com/v1/search'

    def obtener_coordenadas(self, ciudad: str) -> CoordenadasDTO:
        response = requests.get(
            self.BASE_URL,
            params={'name': ciudad, 'count': 1, 'language': 'es', 'format': 'json'},
            timeout=10,
        )
        response.raise_for_status()
        resultados = response.json().get('results')

        if not resultados:
            raise ValueError(f'No se encontraron coordenadas para la ciudad: {ciudad}')

        resultado = resultados[0]
        return CoordenadasDTO(
            latitud=resultado['latitude'],
            longitud=resultado['longitude'],
            ciudad=resultado['name'],
        )