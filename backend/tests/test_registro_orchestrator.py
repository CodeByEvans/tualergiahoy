import pytest
from unittest.mock import Mock
from datetime import datetime

from registro.services.orchestrator import RegistroOrchestrator
from registro.exceptions import AIServiceUnavailableError, SheetsServiceUnavailableError, GeocodingServiceUnavailableError


class FakeUsuario:
    def __init__(self):
        self.first_name = "Evans"
        self.last_name = "Test"
        self.email = "test@test.com"


class FakeRegistro:
    def __init__(self):
        self.id = 1
        self.usuario = FakeUsuario()
        self.fecha_nacimiento = "1995-01-01"
        self.ciudad = "Madrid"
        self.telefono = "123456789"
        self.alergias = [
            {"nombre": "gramineas", "severidad": "alta"}
        ]
        self.medicacion = "antihistamínicos"
        self.acepta_notificaciones = True
        self.como_nos_conocio = "google"
        self.created_at = datetime.now()

    def get_ciudad_display(self):
        return "Madrid"
    
def test_flujo_completo_ok():
    # 🔹 Mocks
    geocoding = Mock()
    pollen = Mock()
    sheets = Mock()
    ai = Mock()
    docs = Mock()
    email = Mock()

    # 🔹 Configurar comportamiento
    geocoding.obtener_coordenadas.return_value = (40.4, -3.7)

    pollen.obtener_datos_polen.return_value = Mock(
        estado="Alto",
        tipo_polen="gramineas",
        datos_detalle="detalle fake"
    )

    ai.generar_prevision.return_value = "prevision fake"

    docs.generar_pdf.return_value = Mock(
        contenido=b"pdf_bytes",
        nombre_archivo="test.pdf"
    )

    # 🔹 Orchestrator
    orchestrator = RegistroOrchestrator(
        geocoding_service=geocoding,
        pollen_service=pollen,
        sheets_service=sheets,
        ai_service=ai,
        docs_service=docs,
        email_service=email,
    )

    registro = FakeRegistro()

    # 🔹 Ejecutar generator
    eventos = list(orchestrator.ejecutar(registro))

    # ✅ Assert 1: terminó correctamente
    assert any("Proceso completado" in e for e in eventos)

    # ✅ Assert 2: email enviado
    email.enviar_bienvenida.assert_called_once()

    # ✅ Assert 3: email tiene PDF
    args, kwargs = email.enviar_bienvenida.call_args
    assert kwargs["pdf"] is not None

def test_IA_no_disponible_devuelve_email_sin_pdf():
    geocoding = Mock()
    pollen = Mock()
    sheets = Mock()
    ai = Mock()
    docs = Mock()
    email = Mock()

    pollen.obtener_datos_polen.return_value = Mock(
        estado="Alto",
        tipo_polen="gramineas",
        datos_detalle="detalle fake"
    )

    ai.generar_prevision.side_effect = AIServiceUnavailableError()

    orchestrator = RegistroOrchestrator(
        geocoding_service=geocoding,
        pollen_service=pollen,
        sheets_service=sheets,
        ai_service=ai,
        docs_service=docs,
        email_service=email,
    )

    registro = FakeRegistro()

    # 🔹 Ejecutar generator
    eventos = list(orchestrator.ejecutar(registro))

    # ✅ Assert 1: terminó correctamente
    assert any("IA no disponible" in e for e in eventos)

    # ✅ Assert 2: email enviado
    email.enviar_bienvenida.assert_called_once()

    # ✅ Assert 3: email no tiene PDF
    args, kwargs = email.enviar_bienvenida.call_args
    assert kwargs["pdf"] is None

def test_sheets_no_funciona_sigue_ejecutando():
    geocoding = Mock()
    pollen = Mock()
    sheets = Mock()
    ai = Mock()
    docs = Mock()
    email = Mock()

    sheets.insertar_registro.side_effect = SheetsServiceUnavailableError()

    orchestrator = RegistroOrchestrator(
        geocoding_service=geocoding,
        pollen_service=pollen,
        sheets_service=sheets,
        ai_service=ai,
        docs_service=docs,
        email_service=email,
    )

    registro = FakeRegistro()

    # 🔹 Ejecutar generator
    eventos = list(orchestrator.ejecutar(registro))

    # ✅ Assert 1: terminó correctamente
    assert any("Proceso completado" in e for e in eventos)

    # ✅ Assert 2: email enviado
    email.enviar_bienvenida.assert_called_once()

    # ✅ Assert 3: email tiene PDF
    args, kwargs = email.enviar_bienvenida.call_args
    assert kwargs["pdf"] is not None

    # ✅ Assert 4: sheets llamada pero no funciona
    sheets.insertar_registro.assert_called_once()

    # ✅ Assert 5: AI llamada
    ai.generar_prevision.assert_called_once()

def test_geocoding_falla_corta_flujo():

    geocoding = Mock()
    pollen = Mock()
    sheets = Mock()
    ai = Mock()
    docs = Mock()
    email = Mock()

    geocoding.obtener_coordenadas.side_effect = GeocodingServiceUnavailableError()

    orchestrator = RegistroOrchestrator(
        geocoding_service=geocoding,
        pollen_service=pollen,
        sheets_service=sheets,
        ai_service=ai,
        docs_service=docs,
        email_service=email,
    )

    registro = FakeRegistro()

    # 🔹 Ejecutar generator
    eventos = list(orchestrator.ejecutar(registro))

    # ✅ Assert 1: terminó correctamente
    assert any("Geocoding service unavailable" in e for e in eventos)

    email.enviar_bienvenida.assert_not_called()
    docs.generar_pdf.assert_not_called()
    ai.generar_prevision.assert_not_called()