# dispositivos/management/commands/cargar_fixtures.py
import os
import sys
import django

# Configurar Django
try:
    current_file = __file__
    commands_dir = os.path.dirname(current_file)
    management_dir = os.path.dirname(commands_dir)
    apps_dir = os.path.dirname(management_dir)
    project_dir = os.path.dirname(apps_dir)
    
    sys.path.insert(0, project_dir)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dulceria.settings')
    django.setup()
    
    from django.core.management.base import BaseCommand
    from django.core.management import call_command
    
except ImportError as e:
    print(f"Error: {e}")
    sys.exit(1)

class Command(BaseCommand):
    help = 'Carga todas las fixtures en orden'

    def handle(self, *args, **options):
        fixtures = [
            '00_proveedores',
            '01_usuarios', 
            '02_perfiles',
            '03_productos'
        ]

        self.stdout.write('Cargando fixtures...')

        for fixture in fixtures:
            self.stdout.write(f'Cargando {fixture}...')
            try:
                call_command('loaddata', fixture)
                self.stdout.write(self.style.SUCCESS(f'[OK] {fixture} cargado'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'[ERROR] en {fixture}: {e}'))

        self.stdout.write(self.style.SUCCESS('[EXITO] Todas las fixtures cargadas!'))