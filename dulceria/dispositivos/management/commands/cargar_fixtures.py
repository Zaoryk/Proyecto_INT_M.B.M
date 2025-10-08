import os
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Carga los fixtures en la base de datos'

    def handle(self, *args, **options):
        fixtures_file = 'fixtures_dulceria.json'
        
        if not os.path.exists(fixtures_file):
            self.stdout.write(
                self.style.ERROR(f'No se encuentra el archivo {fixtures_file}')
            )
            self.stdout.write(
                self.style.WARNING('Ejecuta primero: python manage.py generar_fixtures')
            )
            return
        
        try:
            self.stdout.write(f'Cargando fixtures desde {fixtures_file}...')
            call_command('loaddata', fixtures_file)
            self.stdout.write(
                self.style.SUCCESS('Fixtures cargados exitosamente!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error al cargar fixtures: {e}')
            )