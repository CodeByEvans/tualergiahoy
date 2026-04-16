from django.contrib.auth.hashers import make_password
from django.db import transaction
import phonenumbers
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Registro, Usuario, SeveridadChoices, ComoNosConocioChoices
from .constants import ALERGENO_MAP, PROVINCIA_CHOICES

ALERGENOS_VALIDOS = set(ALERGENO_MAP.keys())

class AlergiaDetalleSerializer(serializers.Serializer):
    nombre = serializers.CharField()
    severidad = serializers.ChoiceField(choices=SeveridadChoices.choices)

class RegistroSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(min_length=2, max_length=50)
    apellidos = serializers.CharField(min_length=2, max_length=50)
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=Usuario.objects.all(),
                message='Este correo ya está registrado',
            )
        ]
    )
    password = serializers.CharField(write_only=True, min_length=8)

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
                raise serializers.ValidationError('El formato de teléfono no es válido.')
            return phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)
        
        except phonenumbers.NumberParseException:
            raise serializers.ValidationError('El formato de teléfono no es válido.')

    def validate_alergias(self, value):
        nombres_alergias = [alergia['nombre'] for alergia in value]

        invalidas = [n for n in nombres_alergias if n not in ALERGENOS_VALIDOS]

        if invalidas:
            raise serializers.ValidationError(f'Alérgenos no reconocidos: {invalidas}')
        return value
    
    @transaction.atomic
    def create(self, validated_data):
        usuario = Usuario.objects.create(
            email=validated_data['email'],
            first_name=validated_data['nombre'],
            last_name=validated_data['apellidos'],
            password=make_password(validated_data['password']),
        )

        registro = Registro.objects.create(
            usuario=usuario,
            fecha_nacimiento=validated_data['fecha_nacimiento'],
            ciudad=validated_data['ciudad'],
            telefono=validated_data.get('telefono'),
            alergias=validated_data['alergias'],
            medicacion=validated_data.get('medicacion', ''),
            acepta_notificaciones=validated_data.get('acepta_notificaciones', False),
            como_nos_conocio=validated_data['como_nos_conocio'],
        )

        return registro