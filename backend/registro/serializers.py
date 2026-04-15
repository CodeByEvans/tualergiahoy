from .constants import ALERGENO_MAP
import phonenumbers
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Registro, SeveridadChoices, ComoNosConocioChoices

ALERGENOS_VALIDOS = set(ALERGENO_MAP.keys())

class AlergiaDetalleSerializer(serializers.Serializer):
    nombre = serializers.CharField()
    severidad = serializers.ChoiceField(choices=SeveridadChoices.choices)

class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    alergias = AlergiaDetalleSerializer(many=True)
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=Registro.objects.all(),
                message='Este correo ya está registrado',
            )
        ]
    )

    class Meta:
        model = Registro
        fields = [
            'nombre', 'apellidos', 'fecha_nacimiento', 'ciudad',
            'email', 'password', 'telefono', 'alergias',
            'medicacion', 'acepta_notificaciones', 'como_nos_conocio',
        ]

    def validate_telefono(self, value):
        if not value:
            return None
        
        try:
            number = phonenumbers.parse(value, 'ES')
            if not phonenumbers.is_valid_number(number):
                raise ValueError
            return phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)
        
        except phonenumbers.NumberParseException:
            raise serializers.ValidationError('El formato de teléfono no es válido.')

    def validate_alergias(self, value):
        nombres_alergias = [alergia['nombre'] for alergia in value]

        invalidas = [n for n in nombres_alergias if n not in ALERGENOS_VALIDOS]

        if invalidas:
            raise serializers.ValidationError(f'Alérgenos no reconocidos: {invalidas}')
        return value