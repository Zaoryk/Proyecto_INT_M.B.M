# dispositivos/management/commands/generar_fixtures.py
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
    from django.core import serializers
    from dispositivos.models import (
        ListarPrecios, Usuario, Producto, OrdenProduccion, Proveedor, 
        OrdenDeCompra, Bodega, MovimientoInventario, Costo, Cliente, Pedido
    )
    
    print("[OK] Módulos importados correctamente")
    
except ImportError as e:
    print(f"[ERROR] Importando módulos: {e}")
    sys.exit(1)

class Command(BaseCommand):
    help = 'Genera archivos fixtures para el nuevo esquema MySQL'

    def handle(self, *args, **options):
        print("=== GENERANDO FIXTURES PARA NUEVO ESQUEMA MYSQL ===")
        
        # Crear directorio de fixtures si no existe
        fixtures_dir = os.path.join('dispositivos', 'fixtures')
        if not os.path.exists(fixtures_dir):
            os.makedirs(fixtures_dir)
            print(f"[OK] Directorio creado: {fixtures_dir}")
        else:
            print(f"[OK] Directorio ya existe: {fixtures_dir}")

        # Primero cargar datos de prueba
        self.generar_datos_prueba()
        
        # Luego exportar a fixtures
        self.exportar_fixtures()
        
        print("[EXITO] Fixtures generados exitosamente!")
        print("Archivos creados en: dispositivos/fixtures/")

    def generar_datos_prueba(self):
        """Genera datos de prueba usando el script actualizado"""
        print("--- Generando datos de prueba ---")
        
        # Usar el script de carga actualizado
        from dispositivos.management.commands.cargar_datos_directo import Command as CargarDatos
        cargador = CargarDatos()
        cargador.handle()

    def exportar_fixtures(self):
        """Exporta los datos a archivos fixtures"""
        print("--- Exportando a archivos JSON ---")
        
        # Exportar en orden de dependencias
        modelos = [
            ('00_clientes.json', Cliente),
            ('01_listas_precios.json', ListarPrecios),
            ('02_usuarios.json', Usuario),
            ('03_proveedores.json', Proveedor),
            ('04_productos.json', Producto),
            ('05_bodegas.json', Bodega),
            ('06_ordenes_compra.json', OrdenDeCompra),
            ('07_ordenes_produccion.json', OrdenProduccion),
            ('08_pedidos.json', Pedido),
            ('09_movimientos_inventario.json', MovimientoInventario),
            ('10_costos.json', Costo),
        ]
        
        for archivo, modelo in modelos:
            try:
                objetos = modelo.objects.all()
                if objetos.exists():
                    with open(f'dispositivos/fixtures/{archivo}', 'w', encoding='utf-8') as f:
                        data = serializers.serialize('json', objetos, indent=2, ensure_ascii=False)
                        f.write(data)
                    print(f"[OK] {archivo} - {objetos.count()} registros")
                else:
                    print(f"[AVISO] {archivo} - Sin datos para exportar")
            except Exception as e:
                print(f"[ERROR] en {archivo}: {e}")