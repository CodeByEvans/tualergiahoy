from datetime import datetime
import json
import time
from django.contrib.auth.hashers import make_password

from ..exceptions import AIServiceUnavaibleError

from .google_auth_service import GoogleAuthService
from ..interfaces import IGeocodingService, IPollenService, ISheetsService, IAIService, IDocsService, IEmailService
from ..services import GeocodingService, PollenService, SheetsService, AIService, DocsService, EmailService
from ..models import Registro


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
        
        auth = GoogleAuthService()  # Para autenticación con Google.

        # Inyección de dependencias — fácil de mockear en tests
        self._geocoding = geocoding_service or GeocodingService()
        self._pollen = pollen_service or PollenService()
        self._sheets = sheets_service or SheetsService()
        self._ai = ai_service or AIService()
        self._docs = docs_service or DocsService(auth_service=auth)
        self._email = email_service or EmailService()

    def ejecutar(self, datos_validados: dict):
        # 1. Persistir en base de datos
        try: 
            yield self._formatear_ev("Guardando tu perfil...", 10)
            registro = Registro.objects.create(
                **{**datos_validados, 'password': make_password(datos_validados['password'])}
            )
    
            # 2. Geocodificar ciudad
            yield self._formatear_ev(f"Localizando {registro.ciudad}...", 25)
            coordenadas = self._geocoding.obtener_coordenadas(registro.ciudad)
    
            # 3. Datos de polen
            yield self._formatear_ev("Obteniendo datos de polen...", 40)
            datos_polen = self._pollen.obtener_datos_polen(
                coordenadas,
                registro.alergias,
            )
    
            # 4. Google Sheets
            alergias_texto = ', '.join([f'{alergia['nombre']} ({alergia["severidad"]})' for alergia in registro.alergias])
            self._sheets.insertar_registro({
                'id': registro.id,
                'nombre': registro.nombre,
                'apellidos': registro.apellidos,
                'fecha_nacimiento': str(registro.fecha_nacimiento),
                'ciudad': registro.get_ciudad_display(),
                'email': registro.email,
                'telefono': registro.telefono,
                'alergias': alergias_texto,
                'medicacion': registro.medicacion,
                'acepta_notificaciones': registro.acepta_notificaciones,
                'nivel_riesgo': datos_polen.estado,
                'como_nos_conocio': registro.como_nos_conocio,
                'fecha_registro': registro.created_at.strftime('%d/%m/%Y %H:%M'),
            })
    
            # 5. Previsión IA
            try:
                yield self._formatear_ev("IA analizando tu caso (esto puede tardar)", 75)
                prevision = self._ai.generar_prevision(
                    nombre=registro.nombre,
                    ciudad=registro.ciudad,
                    alergias=registro.alergias,
                    medicacion=registro.medicacion,
                    datos_polen=datos_polen,
                )
    
                # 6. Generar PDF
                yield self._formatear_ev("Generando tu informe PDF personalizado...", 85)
                semana = datetime.now().strftime('%d/%m/%Y')
                pdf = self._docs.generar_pdf({
                    'NOMBRE': registro.nombre,
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
    
                # 7. Enviar email
                yield self._formatear_ev("Enviando email de bienvenida...", 95)
                self._email.enviar_bienvenida(
                    destinatario=registro.email,
                    nombre=registro.nombre,
                    datos_polen=datos_polen,
                    pdf=pdf,
                )
    
            except AIServiceUnavaibleError:
                yield self._formatear_ev("IA no disponible, enviando email de bienvenida sin PDF...", 95)
                self._email.enviar_bienvenida(
                    destinatario=registro.email,
                    nombre=registro.nombre,
                    datos_polen=datos_polen,
                    pdf= None,
                )
    
            yield self._formatear_ev("¡Proceso completado!", 100, True)
            print("¡Proceso completado!")
        
        except Exception as e:
            yield self._formatear_ev(f"Error: {str(e)}", 100, True)
            print(e)
    
    def _formatear_ev(self, mensaje, progreso, finalizado=False):
        """Helper para estructurar el mensaje SSE"""
        data = {
            "message": mensaje,
            "progress": progreso,
            "done": finalizado
        }
        return f"data: {json.dumps(data)}\n\n"