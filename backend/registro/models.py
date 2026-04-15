import uuid
from django.db import models
from .constants import PROVINCIA_CHOICES


class SeveridadChoices(models.TextChoices):
    LEVE = 'leve', 'Leve'
    MODERADA = 'moderada', 'Moderada'
    SEVERA = 'severa', 'Severa'


class ComoNosConocioChoices(models.TextChoices):
    INSTAGRAM = 'instagram', 'Instagram'
    TIKTOK = 'tiktok', 'TikTok'
    AMIGOS_OTROS = 'amigos_otros', 'Amigos / Otros'


class Registro(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    fecha_nacimiento = models.DateField()
    ciudad = models.CharField(
        max_length=25,
        choices=PROVINCIA_CHOICES,
    )
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255) 
    telefono = models.CharField(max_length=20, blank=True, null=True)

    alergias = models.JSONField(default=list)
    
    medicacion = models.TextField(blank=True, null=True)
    acepta_notificaciones = models.BooleanField(default=False)
    como_nos_conocio = models.CharField(
        max_length=20,
        choices=ComoNosConocioChoices.choices,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Registro'
        verbose_name_plural = 'Registros'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.nombre} {self.apellidos} — {self.email}'

    @property
    def nombre_completo(self):
        return f'{self.nombre} {self.apellidos}'