from unittest.mock import Mock
from registro.services.ai_service import AIService
from registro.exceptions import AIServiceUnavailableError
import pytest

def test_ai_devuelve_texto():
    service = AIService.__new__(AIService) 

    mock_client = Mock()
    service._client = mock_client

    mock_client.models.generate_content.return_value = Mock(text="respuesta IA")

    result = service.generar_prevision(
        nombre="Evans",
        ciudad="Madrid",
        alergias=[{"nombre": "gramineas", "severidad": "alta"}],
        medicacion="nada",
        datos_polen=Mock(tipo_polen="gramineas", estado="Alto", datos_detalle="detalle")
    )

    assert result == "respuesta IA"

def test_ai_lanza_excepcion():
    service = AIService.__new__(AIService) 

    mock_client = Mock()
    service._client = mock_client

    mock_client.models.generate_content.side_effect = Exception("Error IA")
    
    with pytest.raises(AIServiceUnavailableError):
        service.generar_prevision(
            nombre="Evans",
            ciudad="Madrid",
            alergias=[{"nombre": "gramineas", "severidad": "alta"}],
            medicacion="nada",
            datos_polen=Mock(tipo_polen="gramineas", estado="Alto", datos_detalle="detalle")
        )

def test_ai_sin_respuesta():
    service = AIService.__new__(AIService) 

    mock_client = Mock()
    service._client = mock_client

    mock_client.models.generate_content.return_value = Mock(text=None)

    result = service.generar_prevision(
        nombre="Evans",
        ciudad="Madrid",
        alergias=[{"nombre": "gramineas", "severidad": "alta"}],
        medicacion="nada",
        datos_polen=Mock(tipo_polen="gramineas", estado="Alto", datos_detalle="detalle")
    )

    assert result == "Sin respuesta"