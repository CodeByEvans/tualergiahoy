from datetime import datetime
import json
import time

from ..exceptions import AIServiceUnavailableError, SheetsServiceUnavailableError, GeocodingServiceUnavailableError

from .google_auth_service import GoogleAuthService
from ..interfaces import IGeocodingService, IPollenService, ISheetsService, IAIService, IDocsService, IEmailService
from ..services import GeocodingService, PollenService, SheetsService, AIService, DocsService, EmailService
from ..models import Registro
import logging

logger = logging.getLogger(__name__)


class RegistroOrchestrator:
    """
    Coordina el flujo completo de registro:
    1. Persiste en base de datos
    2. Geocodifica la ciudad
    3. Obtiene datos de polen
    4. Escribe en Google Sheets
    5. Genera previsión con IA
    6. Crea PDF desde plantilla
    7. Envía email de bienvenida
    """

    def __init__(
        self,
        geocoding_service: IGeocodingService = None,
        pollen_service: IPollenService = None,
        sheets_service: ISheetsService = None,
        ai_service: IAIService = None,
        docs_service: IDocsService = None,
        email_service: IEmailService = None,
    ):
        
        if docs_service is None:
            auth = GoogleAuthService()
            docs_service = DocsService(auth_service=auth)

        # Inyección de dependencias — fácil de mockear en tests
        self._geocoding = geocoding_service or GeocodingService()
        self._pollen = pollen_service or PollenService()
        self._sheets = sheets_service or SheetsService()
        self._ai = ai_service or AIService()
        self._docs = docs_service
        self._email = email_service or EmailService()

    def ejecutar(self, registro: Registro):
        try: 
            try:
                # 1. Geocodificar ciudad
                yield self._formatear_ev(f"Localizando {registro.ciudad}...", 25)
                coordenadas = self._geocoding.obtener_coordenadas(registro.ciudad)
            except GeocodingServiceUnavailableError as e:
                logger.exception('Geocoding service unavailable', extra={'ciudad': registro.ciudad})
                yield self._formatear_ev('Geocoding service unavailable', 100)
                return
    
            # 2. Datos de polen
            yield self._formatear_ev("Obteniendo datos de polen...", 40)
            datos_polen = self._pollen.obtener_datos_polen(
                coordenadas,
                registro.alergias,
            )

            try:
                # 3. Google Sheets
                alergias_texto = ', '.join(
                    f"{a['nombre']} ({a['severidad']})"
                    for a in registro.alergias
                )   
                self._sheets.insertar_registro({
                    'id': registro.id,
                    'nombre': registro.usuario.first_name,
                    'apellidos': registro.usuario.last_name,
                    'fecha_nacimiento': str(registro.fecha_nacimiento),
                    'ciudad': registro.get_ciudad_display(),
                    'email': registro.usuario.email,
                    'telefono': registro.telefono,
                    'alergias': alergias_texto,
                    'medicacion': registro.medicacion,
                    'acepta_notificaciones': registro.acepta_notificaciones,
                    'nivel_riesgo': datos_polen.estado,
                    'como_nos_conocio': registro.como_nos_conocio,
                    'fecha_registro': registro.created_at.strftime('%d/%m/%Y %H:%M'),
                })
            except SheetsServiceUnavailableError as e:
                logger.exception(
                    "Error al insertar registro en Google Sheets",
                    extra={
                        "registro_id": registro.id,
                        "usuario_email": registro.usuario.email
                    }
                )

    
            # 4. Previsión IA
            try:
                yield self._formatear_ev("IA analizando tu caso (esto puede tardar)", 75)
                prevision = self._ai.generar_prevision(
                    nombre=registro.usuario.first_name,
                    ciudad=registro.ciudad,
                    alergias=registro.alergias,
                    medicacion=registro.medicacion,
                    datos_polen=datos_polen,
                )
    
                # 5. Generar PDF
                yield self._formatear_ev("Generando tu informe PDF personalizado...", 85)
                semana = datetime.now().strftime('%d/%m/%Y')
                pdf = self._docs.generar_pdf({
                    'NOMBRE': registro.usuario.first_name,
                    'FECHA_SEMANA': semana,
                    'PREVISION_IA': prevision,
                    'CIUDAD': registro.get_ciudad_display(),
                    'ZONA_MUESTREO': f'{registro.ciudad} (Modelo CAMS Europeo)',
                    'ESTADO': datos_polen.estado,
                    'TIPO_POLEN': datos_polen.tipo_polen,
                    'DATOS_POLEN': datos_polen.datos_detalle,
                    'ALERGIAS': alergias_texto,
                    'MEDICACION': registro.medicacion or 'Ninguna',
                    'NOTIFICACIONES': 'Sí' if registro.acepta_notificaciones else 'No',
                })

    
                # 6. Enviar email
                yield self._formatear_ev("Enviando email de bienvenida...", 95)
                self._email.enviar_bienvenida(
                    destinatario=registro.usuario.email,
                    nombre=registro.usuario.first_name,
                    datos_polen=datos_polen,
                    pdf=pdf,
                )
    
            except AIServiceUnavailableError:
                yield self._formatear_ev("IA no disponible, enviando email de bienvenida sin PDF...", 95)
                self._email.enviar_bienvenida(
                    destinatario=registro.usuario.email,
                    nombre=registro.usuario.first_name,
                    datos_polen=datos_polen,
                    pdf= None,
                )
    
            yield self._formatear_ev("¡Proceso completado!", 100, True)
        
        except Exception as e:
            yield self._formatear_ev(f"Error: {str(e)}", 100, True)
    
    def _formatear_ev(self, mensaje, progreso, finalizado=False):
        """Helper para estructurar el mensaje SSE"""
        data = {
            "message": mensaje,
            "progress": progreso,
            "done": finalizado
        }
        return f"data: {json.dumps(data)}\n\n"