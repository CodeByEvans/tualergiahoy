from django.core.management.base import BaseCommand
from registro.models import Registro, Usuario


class Command(BaseCommand):
    help = 'Elimina datos de prueba'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Email a eliminar')
        parser.add_argument('--todos', action='store_true', help='Borra todo')

    def handle(self, *args, **options):
        if options['todos']:
            usuarios = Usuario.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(
                f'Eliminados todos los usuarios (y sus registros)'
            ))
            return

        email = options['email']

        if not email:
            self.stdout.write(self.style.ERROR('Debes usar --email o --todos'))
            return

        deleted, _ = Usuario.objects.filter(email=email).delete()

        self.stdout.write(self.style.SUCCESS(
            f'Eliminado usuario {email} (y su registro asociado)'
        ))