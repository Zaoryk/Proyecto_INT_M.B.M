# dispositivos/management/commands/cargar_fixtures.py
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
    help = 'Carga todas las fixtures en orden para nuevo esquema'

    def handle(self, *args, **options):
        print("=== CARGANDO FIXTURES PARA NUEVO ESQUEMA MYSQL ===")
        
        fixtures = [
            '00_clientes',
            '01_listas_precios',
            '02_usuarios',
            '03_proveedores',
            '04_productos',
            '05_bodegas',
            '06_ordenes_compra',
            '07_ordenes_produccion',
            '08_pedidos',
            '09_movimientos_inventario',
            '10_costos'
        ]

        for fixture in fixtures:
            print(f"Cargando {fixture}...")
            try:
                call_command('loaddata', fixture)
                print(f"[OK] {fixture} cargado")
            except Exception as e:
                print(f"[ERROR] en {fixture}: {e}")

        print("[EXITO] Todas las fixtures cargadas")