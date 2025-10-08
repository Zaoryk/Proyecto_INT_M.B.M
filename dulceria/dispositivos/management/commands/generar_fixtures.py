import json
from datetime import date
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Genera fixtures para la dulcería Lilis'

    def handle(self, *args, **options):
        fixtures = []
        
        # Bodegas
        bodegas = [
            {"model": "dispositivos.bodega", "pk": 1, "fields": {"nombre": "BOD-CENTRAL", "ubicacion": "La Serena"}},
            {"model": "dispositivos.bodega", "pk": 2, "fields": {"nombre": "BOD-SUR", "ubicacion": "Ovalle"}},
        ]
        fixtures.extend(bodegas)
        
        # Clientes
        clientes = [
            {"model": "dispositivos.cliente", "pk": 1, "fields": {"nombre": "Supermercado Lider", "tipo": "Minorista"}},
            {"model": "dispositivos.cliente", "pk": 2, "fields": {"nombre": "Feria La Serena", "tipo": "Mayorista"}},
        ]
        fixtures.extend(clientes)
        
        # Proveedores
        proveedores = [
            {"model": "dispositivos.proveedor", "pk": 1, "fields": {"nombre": "Proveedor Andino S.A.", "contacto": "Juan Pérez", "email": "contacto@andino.cl"}},
            {"model": "dispositivos.proveedor", "pk": 2, "fields": {"nombre": "Electro Patagon SpA", "contacto": "María González", "email": "ventas@electropatagon.cl"}},
        ]
        fixtures.extend(proveedores)
        
        # Productos
        productos = [
            {"model": "dispositivos.producto", "pk": 1, "fields": {"nombre": "Chocolate Amargo 100g", "lote": "LOTE-CHOC-001", "fecha_vencimiento": "2025-12-31", "precio": 1500, "stock": 50}},
            {"model": "dispositivos.producto", "pk": 2, "fields": {"nombre": "Caramelo Frutal 500g", "lote": "LOTE-CAR-001", "fecha_vencimiento": "2025-10-15", "precio": 800, "stock": 100}},
        ]
        fixtures.extend(productos)
        
        # ListarPrecios
        listar_precios = [
            {"model": "dispositivos.listarprecios", "pk": 1, "fields": {"canal": "Minorista", "temporada": "Normal", "valor": 1500, "cliente": 1}},
            {"model": "dispositivos.listarprecios", "pk": 2, "fields": {"canal": "Mayorista", "temporada": "Promoción", "valor": 1300, "cliente": 2}},
        ]
        fixtures.extend(listar_precios)
        
        # Usuarios (SIN el campo listarprecios_idlistarprecios)
        usuarios = [
            {"model": "dispositivos.usuario", "pk": 1, "fields": {"nombre": "Admin Principal", "rol": "administrador", "password": "pbkdf2_sha256$600000$TEST$TEST", "email": "admin@dulcerialilis.cl"}},
            {"model": "dispositivos.usuario", "pk": 2, "fields": {"nombre": "Operador Inventario", "rol": "operador_inventario", "password": "pbkdf2_sha256$600000$TEST$TEST", "email": "inventario@dulcerialilis.cl"}},
        ]
        fixtures.extend(usuarios)
        
        # Resto del código permanece igual...
        # Costos
        costos = [
            {"model": "dispositivos.costo", "pk": 1, "fields": {"tipo": "Producción", "monto": 800, "producto": 1}},
            {"model": "dispositivos.costo", "pk": 2, "fields": {"tipo": "Embalaje", "monto": 150, "producto": 1}},
        ]
        fixtures.extend(costos)
        
        # MovimientosInventario
        movimientos = [
            {"model": "dispositivos.movimientoinventario", "pk": 1, "fields": {"tipo": "Ingreso", "fecha": "2025-01-15", "cantidad": "100", "bodega": 1, "producto": 1}},
            {"model": "dispositivos.movimientoinventario", "pk": 2, "fields": {"tipo": "Salida", "fecha": "2025-01-20", "cantidad": "50", "bodega": 1, "producto": 1}},
        ]
        fixtures.extend(movimientos)
        
        # OrdenesDeCompra
        ordenes_compra = [
            {"model": "dispositivos.ordendecompra", "pk": 1, "fields": {"fecha": "2025-01-05", "estado": "cerrada", "monto_total": 150000, "proveedor": 1}},
            {"model": "dispositivos.ordendecompra", "pk": 2, "fields": {"fecha": "2025-01-18", "estado": "en_proceso", "monto_total": 80000, "proveedor": 2}},
        ]
        fixtures.extend(ordenes_compra)
        
        # OrdenesProduccion
        ordenes_produccion = [
            {"model": "dispositivos.ordenproduccion", "pk": 1, "fields": {"fechainicio": "2025-01-01", "fechafin": "2025-01-10", "estado": "Completada", "usuario": 2, "producto": 1}},
        ]
        fixtures.extend(ordenes_produccion)
        
        # Pedidos
        pedidos = [
            {"model": "dispositivos.pedido", "pk": 1, "fields": {"fecha": "2025-01-12", "monto_total": 45000, "usuario": 1, "cliente": 1, "ordendecompra": 1}},
        ]
        fixtures.extend(pedidos)
        
        # Guardar fixtures
        with open('fixtures_dulceria.json', 'w', encoding='utf-8') as f:
            json.dump(fixtures, f, indent=2, ensure_ascii=False)
        
        self.stdout.write(
            self.style.SUCCESS(f'Fixtures generados: {len(fixtures)} registros en fixtures_dulceria.json')
        )