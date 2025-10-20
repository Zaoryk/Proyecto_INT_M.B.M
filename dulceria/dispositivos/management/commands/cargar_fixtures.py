import os
import json
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction

class Command(BaseCommand):
    help = 'Carga los fixtures en la base de datos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fixture-file',
            type=str,
            default='fixtures_dulceria.json',
            help='Nombre del archivo fixture a cargar (por defecto: fixtures_dulceria.json)'
        )
        parser.add_argument(
            '--skip-verification',
            action='store_true',
            help='Omite la verificación del contenido del fixture'
        )

    def handle(self, *args, **options):
        fixture_file = options['fixture_file']
        skip_verification = options['skip_verification']
        
        if not os.path.exists(fixture_file):
            self.stdout.write(
                self.style.ERROR(f'No se encuentra el archivo {fixture_file}')
            )
            self.stdout.write(
                self.style.WARNING('Ejecuta primero: python manage.py generar_fixtures')
            )
            self.stdout.write(
                self.style.WARNING('O especifica otro archivo con: python manage.py cargar_fixtures --fixture-file mi_fixture.json')
            )
            return
        
        # Verificar que el archivo fixture tenga contenido válido
        if not skip_verification:
            if not self.verificar_fixture(fixture_file):
                self.stdout.write(
                    self.style.ERROR('El archivo fixture no es válido. No se cargarán los datos.')
                )
                return
        
        try:
            self.stdout.write(f'Cargando fixtures desde {fixture_file}...')
            
            # Contar registros antes de cargar
            total_registros = self.contar_registros_fixture(fixture_file)
            self.stdout.write(f'Se cargarán {total_registros} registros...')
            
            # Cargar fixtures dentro de una transacción
            with transaction.atomic():
                call_command('loaddata', fixture_file)
            
            self.stdout.write(
                self.style.SUCCESS('✓ Fixtures cargados exitosamente!')
            )
            
            # Mostrar resumen de lo cargado
            self.mostrar_resumen(fixture_file)
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Error al cargar fixtures: {str(e)}')
            )
            self.stdout.write(
                self.style.WARNING('La transacción fue revertida. No se cargó ningún dato.')
            )

    def verificar_fixture(self, fixture_file):
        """Verifica que el archivo fixture tenga un formato válido"""
        try:
            with open(fixture_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                self.stdout.write(
                    self.style.ERROR('El fixture debe ser una lista de objetos JSON')
                )
                return False
            
            # Verificar estructura básica de cada elemento
            for i, item in enumerate(data):
                if not isinstance(item, dict):
                    self.stdout.write(
                        self.style.ERROR(f'Elemento {i} no es un objeto JSON válido')
                    )
                    return False
                
                if 'model' not in item or 'pk' not in item or 'fields' not in item:
                    self.stdout.write(
                        self.style.ERROR(f'Elemento {i} no tiene la estructura requerida (model, pk, fields)')
                    )
                    return False
            
            self.stdout.write(
                self.style.SUCCESS('✓ Estructura del fixture verificada correctamente')
            )
            return True
            
        except json.JSONDecodeError as e:
            self.stdout.write(
                self.style.ERROR(f'El archivo fixture no es un JSON válido: {e}')
            )
            return False
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error al verificar el fixture: {e}')
            )
            return False

    def contar_registros_fixture(self, fixture_file):
        """Cuenta el número total de registros en el fixture"""
        try:
            with open(fixture_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return len(data)
        except:
            return 0

    def mostrar_resumen(self, fixture_file):
        """Muestra un resumen de los datos cargados"""
        try:
            with open(fixture_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Contar por modelo
            modelos = {}
            for item in data:
                modelo = item['model']
                if modelo not in modelos:
                    modelos[modelo] = 0
                modelos[modelo] += 1
            
            self.stdout.write("\n" + "="*50)
            self.stdout.write(self.style.SUCCESS("RESUMEN DE DATOS CARGADOS"))
            self.stdout.write("="*50)
            
            for modelo, cantidad in sorted(modelos.items()):
                nombre_legible = modelo.replace('dispositivos.', '').title()
                self.stdout.write(f"  {nombre_legible}: {cantidad} registros")
            
            self.stdout.write("="*50)
            self.stdout.write(self.style.SUCCESS(f"Total: {len(data)} registros cargados"))
            
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'No se pudo generar el resumen: {e}')
            )