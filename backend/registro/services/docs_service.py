import io
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from django.conf import settings
from ..interfaces import IDocsService, IGoogleAuthService
from ..dtos import PDFResultDTO

from .google_auth_service import GoogleAuthService

SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive',
]


class DocsService(IDocsService):
    def __init__(self, auth_service: IGoogleAuthService = None):
        self._auth_service = auth_service or GoogleAuthService()
        creds = self._auth_service.obtener_credenciales()
        self._docs = build('docs', 'v1', credentials=creds)
        self._drive = build('drive', 'v3', credentials=creds)

    def _copiar_plantilla(self, nombre: str) -> str:
        """Crea una copia de la plantilla y devuelve su ID."""
        copia = self._drive.files().copy(
            fileId=settings.GOOGLE_DOCS_TEMPLATE_ID,
            body={'name': nombre, 'parents': [settings.GOOGLE_DRIVE_FOLDER_ID]},
        ).execute()
        return copia['id']

    def _reemplazar_placeholders(self, doc_id: str, reemplazos: dict) -> None:
        """Reemplaza todos los {{PLACEHOLDER}} en el documento."""
        requests = [
            {
                'replaceAllText': {
                    'containsText': {'text': f'{{{{{clave}}}}}', 'matchCase': True},
                    'replaceText': str(valor),
                }
            }
            for clave, valor in reemplazos.items()
        ]
        self._docs.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': requests},
        ).execute()

    def _exportar_pdf(self, doc_id: str) -> bytes:
        """Exporta el documento a PDF y devuelve los bytes."""
        request = self._drive.files().export_media(
            fileId=doc_id,
            mimeType='application/pdf',
        )
        buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(buffer, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        return buffer.getvalue()

    def _eliminar_copia(self, doc_id: str) -> None:
        """Elimina la copia temporal del Drive."""
        self._drive.files().delete(fileId=doc_id).execute()

    def generar_pdf(self, datos_plantilla: dict) -> PDFResultDTO:
        nombre_doc = f"Prevision_{datos_plantilla.get('NOMBRE', 'usuario')}_{datetime.now().strftime('%Y%m%d')}"
        doc_id = self._copiar_plantilla(nombre_doc)

        try:
            self._reemplazar_placeholders(doc_id, datos_plantilla)
            pdf_bytes = self._exportar_pdf(doc_id)
        finally:
            # Siempre limpiamos la copia del Drive aunque falle
            self._eliminar_copia(doc_id)

        return PDFResultDTO(
            contenido=pdf_bytes,
            nombre_archivo=f'{nombre_doc}.pdf',
        )