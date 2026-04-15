from django.core.management.base import BaseCommand

from registro.models import Registro

class Command(BaseCommand):
    help = 'Elimina registros de prueba en la base de datos'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Email del registro a eliminar')
        parser.add_argument('--todos', action='store_true', help='Elimina todos los registros de prueba')

    def handle(self, *args, **options):
        if options['todos']:
            count, _ = Registro.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Eliminados {count} registros de prueba'))
        else:
            email = options['email']
            count, _ = Registro.objects.filter(email=email).delete()
            self.stdout.write(self.style.SUCCESS(f'Eliminados {count} registros de prueba con email {email}'))