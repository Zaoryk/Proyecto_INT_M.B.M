import os
import sys
import django

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
    help = 'Carga todas las fixtures en orden para nuevos modelos'

    def handle(self, *args, **options):
        print("=== CARGANDO FIXTURES PARA NUEVOS MODELOS ===")
        
        fixtures = [
            '00_usuarios',
            '01_proveedores', 
            '02_productos',
            '03_bodegas',
            '04_clientes',
            '05_pedidos_venta'
        ]

        for fixture in fixtures:
            print(f"Cargando {fixture}...")
            try:
                call_command('loaddata', fixture)
                print(f"[OK] {fixture} cargado")
            except Exception as e:
                print(f"[ERROR] en {fixture}: {e}")

        print("[EXITO] Todas las fixtures cargadas")