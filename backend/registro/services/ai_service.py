from google import genai
from datetime import datetime
from django.conf import settings

from ..exceptions import AIServiceUnavailableError

from ..dtos import PollenDTO
from ..interfaces import IAIService


ESTACIONES = {
    (3, 4, 5): 'primavera',
    (6, 7, 8): 'verano',
    (9, 10, 11): 'otoño',
    (12, 1, 2): 'invierno',
}


def _estacion_actual() -> str:
    mes = datetime.now().month
    return next(
        nombre for meses, nombre in ESTACIONES.items() if mes in meses
    )


class AIService(IAIService):
    def __init__(self):
        self._client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def generar_prevision(
        self,
        nombre: str,
        ciudad: str,
        alergias: list[dict],
        medicacion: str,
        datos_polen: PollenDTO,
    ) -> str:
        estacion = _estacion_actual()
        alergias_detalladas = ", ".join([f"{alergia['nombre']} ({alergia['severidad']})" for alergia in alergias])

        prompt = f"""Eres un especialista en salud respiratoria, alergología y bienestar.
Redacta un pronóstico personalizado para la semana en curso para un paciente con las siguientes características:

- Nombre: {nombre}
- Ciudad: {ciudad}
- Estación del año: {estacion}
- Perfíl de alergias: {alergias_detalladas}
- Situación actual: El alérgeno con mayor presencia es {datos_polen.tipo_polen} con un riesgo {datos_polen.estado}
- Detalle ambiental: {datos_polen.datos_detalle}
- Medicación actual: {medicacion}

El texto debe:
- Tener un tono cercano, empático y profesional
- Estar estructurado en 3 párrafos de máximo 4 líneas cada uno
- Incluir recomendaciones prácticas adaptadas a la estación y los niveles de polen actuales
- No usar listas ni bullets, solo párrafos continuos
- No exceder las 250 palabras en total

REGLAS DE SEGURIDAD MÉDICA:
- TIenes prohibido recomendar medicamentos específicos o cambiar dosis.
- Si el usuario ya toma medicación, limítate a recordarle que sea constante con su tratamiento actual.
- Si el usuario NO medicación, y su riesgo es alto, sugiérele consultar con un especialista, pero nunca nombres fármacos.

INSTRUCCIONES ADICIONALES:
1. Si el usuario tiene alguna alergia 'Severa', esas alergias deben tener prioridad en el informe. 
2. Valora las condiciones ambientales para las alergias severas y aconseja las medidas adecuadas.
3. Las alergias moderadas son la segunda prioridad y deben tener un tono de consejo.
4. Para las alergias 'Leves', da consejos de mantenimiento pero no les dediques más de una frase.
5. Nunca alarmes al usuario sobre el riesgo de alergias severas.

Escribe directamente el texto sin saludos previos ni introducción."""

        try:
            mensaje = self._client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt
            )
            return mensaje.text or "Sin respuesta"
        except Exception as e:
            raise AIServiceUnavailableError(str(e))