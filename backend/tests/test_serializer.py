from registro.serializers import RegistroSerializer

def test_serializer_rechaza_ciudad_vacia():
    data = {
        "ciudad": "",
        "alergias": [{"nombre": "gramineas", "severidad": "alta"}],
    }

    serializer = RegistroSerializer(data=data)

    assert not serializer.is_valid()
    assert "ciudad" in serializer.errors

def test_serializer_rechaza_ciudad_inválida():
    data = {
        "ciudad": "Roma",
        "alergias": [{"nombre": "gramineas", "severidad": "alta"}],
    }

    serializer = RegistroSerializer(data=data)

    assert not serializer.is_valid()
    assert "ciudad" in serializer.errors

def test_serializer_rechaza_alergias_mal_formadas():
    data = {
        "ciudad": "Madrid",
        "alergias": "esto_no_es_una_lista",
    }

    serializer = RegistroSerializer(data=data)

    assert not serializer.is_valid()
    assert "alergias" in serializer.errors

def test_serializer_rechaza_sin_campos_obligatorios():
    data = {}

    serializer = RegistroSerializer(data=data)

    assert not serializer.is_valid()
    assert "ciudad" in serializer.errors